import os
import pandasql as ps

import datamonk.scriptorium.storage.gcp as gcp
import datamonk.utils.functions as utils
import datamonk.scriptorium.apps.slack as slack

import logging
logger=logging.getLogger(__name__)


# <editor-fold desc="Prepare environment">


context = {"run_timestamp": utils.time.today(granularity="datetime"),
           "clients":{"bigQuery":gcp.bigQuery(project_id=os.environ["GOOGLE_PROJECT_ID"]),
                      "slack":slack.instance(token=os.environ["SLACK_BOT_TOKEN"])
                      },
           "objects":{}
           }
context["objects"]["monitoring_table"] = context["clients"]["bigQuery"].table(dataset_id="L1_DATA_MODEL", table_id="monitoring", bq_client=context["clients"]["bigQuery"])

# </editor-fold>

# <editor-fold desc="Define functions">
def construct_query(config_dict,**kwargs):
    """
    tabulka
    date
    column
    co
    vyfiltrovat = hodnoty
    za
    WHERE
    jak
    agregovat
    AVG
    jaké
    okno(daily / monthly / yearly)
    """
    voi_config = config_dict["voi"]
    test = config_dict["test"]
    voi_config["filters"] = voi_config["filters"] if "filters" in voi_config else "TRUE"
    if "incremental_filter" in voi_config:
        if voi_config["incremental_filter"] == 'True' and kwargs["monitoring_table"].exists:
            voi_config["filters"] = \
                "{filters} AND CAST({id} AS STRING) NOT IN (SELECT DISTINCT {id} FROM {monitoring_table})".format(
                    filters=voi_config["filters"],
                    id=voi_config["id"],
                    monitoring_table=kwargs["monitoring_table"].path
                )

    if test["type"] == "time_series_fix":
        def window_query(time_dimension):
            return {'daily': '',
                    'weekly': 'OVER (PARTITION BY EXTRACT(YEAR FROM {date})||EXTRACT(WEEK FROM {date}) ORDER BY {date})'
                    .format(
                        date=voi_config["time_dimension"]),
                    'monthly': 'OVER (PARTITION BY EXTRACT(YEAR FROM {date})||EXTRACT(MONTH FROM {date}) ORDER BY {'
                               'date})'.format(
                        date=voi_config["time_dimension"]),
                    'yearly': 'OVER (PARTITION BY EXTRACT(YEAR FROM {date}) ORDER BY {date})'.format(
                        date=voi_config["time_dimension"])}

        window_string = window_query([voi_config["time_dimension"]])[voi_config["granularity"]]

        query = """SELECT {time_dimension}
        ,{aggregation}({metric}) {window} AS {metric}
        FROM {table}
        WHERE {filters}
        GROUP BY {time_dimension} 
        """.format(time_dimension=voi_config["time_dimension"],
                   metric=voi_config["measure"],
                   window=window_string,
                   aggregation=voi_config["aggregation"],
                   table=voi_config["table"],
                   filters=voi_config["filters"] if voi_config["filters"] != '' else "TRUE"
                   )
    else:
        query = """
        SELECT {id},{context_dimensions},{measures}
        FROM {table}
        WHERE {filters}
        """.format(id=voi_config["id"],
                   measures=', '.join(voi_config["measure"]),
                   table=voi_config["table"],
                   context_dimensions=', '.join(voi_config["context_dimensions"]),
                   filters=voi_config["filters"])

    return query

def construct_notification_message(message,table):
    import re
    output = message
    iterations = re.findall(r"\[(.*)\]", message)
    if iterations:
        for iteration in iterations:
            output = output.replace(iteration, '')
            columns = re.findall(r"\{(\w+)\}", iteration)
            iteration_output = "\n".join(
                [iteration.format(**j) for j in table[columns].to_dict("records")])
            output = output.split("[]")
            output.insert(1, iteration_output)
            output = "\n".join(output)
    return output


def run(request="request",
            rules_list="",
            monitoring_table=context["objects"]["monitoring_table"]):
    # <editor-fold desc="Prepare general objects">
    context["objects"]["rules_list"] = rules_list

    logger.info(msg="context:{}".format(str(context)))
    data_input = {}
    testing = {}
    # </editor-fold>
    for rule in rules_list:
        if rule["active"] == 'True':
            logger.info(msg="start processing rule config object:{}".format(str(rule)))
            # <editor-fold desc="Construct query based on rule and get data from source">
            data_input["query"] = construct_query(rule,monitoring_table=monitoring_table)
            data_input_table = context["clients"]["bigQuery"].query(data_input["query"])
            # </editor-fold>

            # <editor-fold desc="Setup testing and test based on conditions">
            testing["config"] = rule["test"]
            testing["query"] = "SELECT id,iif(" + ' AND '.join(
                utils.dictionary(testing["config"]["rules"]).get_elements(
                    "b")) + ",TRUE,FALSE) AS is_condition_met FROM data_input_table"
            testing["columns"] = utils.dictionary(testing["config"]["rules"]).get_elements("k")
            testing["table"] = ps.sqldf(testing["query"])
            # </editor-fold>

            # <editor-fold desc="Create data output table">
            data_output = {"notifications": {}, "log": {}}
            data_output["notifications"]["table"] = data_input_table.merge(testing["table"], how="inner", on="id")
            data_output["notifications"]["table"]["id"] = data_output["notifications"]["table"]["id"].astype(str)
            data_output["notifications"]["table"]["rule_id_version"] = rule["rule_id"] + "_" + rule["version"]
            data_output["notifications"]["table"]["event_type"] = testing["config"]["type"]
            data_output["notifications"]["table"]["timestamp"] = context["run_timestamp"]

            # convert testing colums values to key-value pairs
            data_output["notifications"]["table"]["event_params"] = [
                [{'key': k, 'value': str(v)} for k, v in d.items()]
                for d in data_output["notifications"]["table"][testing["columns"]].to_dict("records")
            ]
            data_output["log"]["table"] = data_output["notifications"]["table"].drop(
                testing["columns"] + rule["voi"]["context_dimensions"], axis=1)
            data_output["notifications"]["table"] = data_output["notifications"]["table"][
                data_output["notifications"]["table"]["is_condition_met"] == 1]

            # </editor-fold>

            # fig = output.plot.line(x="date", y="costs", title="Costs by Platform")

            # <editor-fold desc="Save log and notifications">
            data_output["log"]["records"] = len(data_output["log"]["table"])
            data_output["notifications"]["records"] = len(data_output["notifications"]["table"])

            logger.info(msg="entries to evaluate:{}".format(data_output["log"]["records"]))

            if data_output["log"]["records"] > 0:
                monitoring_table.upload(data_output["log"]["table"].to_dict("records"),
                                        config_object={"schema": monitoring_table.schema},
                                        create_nonexisting_table=True)

            logger.info(msg="entries went through notification:{}".format(data_output["notifications"]["records"]))
            if data_output["notifications"]["records"] > 0:
                if "slack" in rule["notifications"]:
                    logger.info(msg="prepare sending slack message")
                    data_output["notifications"]["slack_message"] = construct_notification_message(
                        message=rule["notifications"]["slack"]["message"],
                        table=data_output["notifications"]["table"]
                    )

                    context["clients"]["slack"].send_message(
                        rule["notifications"]["slack"]["channel"],
                        data_output["notifications"]["slack_message"]

                    )
    return "success"
    # </editor-fold>


# </editor-fold>

# <editor-fold desc="Notes">
# TODO: připravit na apku, do které se budou lidi přihlašovat?

# TODO: připravit streamlit na vkládání inputu

# TODO: připravit sledování outliers v čase na základě pevných podmínek
# USE CASES
# chci monitorovat denní metriky (propad/výrazné navýšení v nějaké metrice), plnění KPIs (jednoduchý threshold)
# plnění měsíčních metrik (budget/přinesené tržby/leads)

# config[voi]: table,time dimension, metrics, type of agg,
# transformační vrstva
# - granularita (transformace => moving averages, only day, summarize whole month(week), count/

# TODO: připravit grafický output
# pd.options.plotting.backend = "plotly"

# </editor-fold>


