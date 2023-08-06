import json
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import bigquery_storage
import logging
import numpy as np
import datamonk.utils.functions as utls
import pandas
import io
import os


class cloudStorage:
    def __init__(self,bucket_name,path_prefix=''):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)
        self.path_prefix = path_prefix
        self.blob_list=self.bucket.list_blobs(prefix=path_prefix)


    def get_blob(self, gcs_path,filename=''):
        blob = self.bucket.blob(gcs_path)
        if filename == '':
            return blob.download_as_string()
        else:
            blob.download_to_filename(filename)

    def get_last_blob(self,filename=''):
        last_file = max([blob.name for blob in self.blob_list])
        return self.get_blob(gcs_path=last_file,filename=filename)

    def upload_blob(self,path, content, content_type,input_type='file'):
      """Uploads a file to the bucket."""

      blob = self.bucket.blob(path)
      if input_type == 'file':
        blob.upload_from_file(content)
      elif input_type == 'string':
        blob.upload_from_string(content, content_type=content_type)

    def upload_utilJSON(self,json_path,gcp_path):
      """Uploads a file to the bucket."""

      blob = self.bucket.blob("utils/"+gcp_path)
      with open(json_path,"rb") as json_file:
        blob.upload_from_file(json_file)
      #blob.upload_from_string(content, content_type=content_type)


    def download_configJSON(self,config_name):
        """Downloads the config file from config directory in Cloud Storage and returns it as a JSON."""
        logging.info('Downloading config file:' + config_name)

        blob = storage.blob.Blob('utils/configs/' + config_name + '.json', self.bucket)
        output_string = blob.download_as_string()

        output_json = json.loads(output_string)
        logging.info("--------SUCCESS------------")
        return output_json

    def download_keysJSON(self,keys_name):
        """Downloads the config file from config directory in Cloud Storage and returns it as a JSON."""
        logging.info('Downloading config file:' + keys_name)

        blob = storage.blob.Blob('utils/keys/' + keys_name + '.json', self.bucket)
        output_string = blob.download_as_string()

        output_json = json.loads(output_string)
        logging.info("--------SUCCESS------------")
        return output_json

class bigQuery(object):
    def __init__(self,project_id):
        self.project_id = project_id
        self.client = bigquery.Client()
        self.storageclient = bigquery_storage.BigQueryReadClient()
        logging.info("BQ client instance running")

    def query(self,query_string,output_type="dataframe"):
        logging.info("BQ QUERY: statement")
        logging.info("--------------")
        logging.info(query_string)
        logging.info("--------------")
        query_job = self.client.query(query_string).result()
        output_data = query_job.to_dataframe(bqstorage_client=self.storageclient)
        if output_type=="json":
            output_data=output_data.to_json()
        return output_data

    @staticmethod
    def map_dict_to_schema(source_dict, **kwargs):
        from google.cloud.bigquery.schema import SchemaField
        from collections import OrderedDict
        import datetime
        import uuid
        NoneType = type(None)

        # FieldType Map Dictionary

        field_type = {
            str: 'STRING',
            bytes: 'BYTES',
            int: 'INTEGER',
            float: 'FLOAT',
            bool: 'BOOLEAN',
            datetime.datetime: 'TIMESTAMP',
            datetime.date: 'DATE',
            datetime.time: 'TIME',
            dict: 'RECORD',
            OrderedDict: 'RECORD',
            uuid.UUID:"STRING",
            NoneType:"STRING"


        }
        # SchemaField list
        schema = []
        # Iterate the existing dictionary
        for key, value in source_dict.items():
            try:
                schemaField = SchemaField(key, field_type[type(value)],description=None)  # NULLABLE BY DEFAULT
            except KeyError:

                # We are expecting a REPEATED field
                if value and len(value) > 0:
                    schemaField = SchemaField(key, field_type[type(value[0])], mode='REPEATED')  # REPEATED

            # Add the field to the list of fields
            schema.append(schemaField)

            # If it is a STRUCT / RECORD field we start the recursion
            if schemaField.field_type == 'RECORD':
                if schemaField.mode == 'REPEATED':
                    schemaField._fields = bigQuery.map_dict_to_schema(value[0])
                else:
                    schemaField._fields = bigQuery.map_dict_to_schema(value)

        # Return the dictionary values

        return schema
    @staticmethod
    def convert_schema_to_dict(schema):
        dict = {}
        data_type_conversions = {
            'STRING': 'str',
            'INTEGER': 'int',
            'BYTES': 'bytes',
            'INTEGER': 'int',
            'FLOAT': 'float',
            'BOOLEAN': 'bool',
            'TIMESTAMP': 'datetime.datetime',
            'DATE': 'datetime.date',
            'TIME': 'datetime.time',
        }

        # Iterate the existing dictionary
        for i in schema:
            if "fields" not in i:
                dict[i["name"]] = data_type_conversions[i["type"]]
            else:
                dict[i["name"]] = bigQuery.convert_schema_to_dict(i["fields"])

            if i["mode"] == "REPEATED":
                dict[i["name"]] = [dict[i["name"]]]

        return dict

    class table():
        def __init__(self,dataset_id,table_id,bq_client,**kwargs):

            self.bq_client=bq_client.client
            self.table_id=table_id
            self.dataset_id=dataset_id
            self.project_id=bq_client.project_id
            self.path="{}.{}.{}".format(self.project_id,self.dataset_id,self.table_id)

            from google.cloud.exceptions import NotFound
            try:
                self.table=self.bq_client.get_table(self.path)
                self.exists = True
                self.schema = self.table.schema
                f = io.StringIO("")
                self.bq_client.schema_to_json(self.schema, f)
                self.schema_dict = bigQuery.convert_schema_to_dict(json.loads(f.getvalue()))
                if "output" in kwargs:
                    if kwargs["output"] == "pandas":
                        output = bigQuery.query(self.bq_client, query_string="SELECT * FROM {}".format(self.path),
                                                output="dataframe")

                    self.output = output

                logging.info("BQ Table" + self.path + " exists")
            except NotFound:
                self.exists = False
                logging.warning("BQ Table " + self.path + " DOES NOT EXIST")


        def get_lastValue(self, column):
            logging.info("BQ: Getting last value of column "+column+" in table "+self.path)
            query = utls.query.get_last_value(column=column, tablePath=self.path)

            query_job = self.bq_client.query(query)
            rows_df = query_job.result().to_dataframe()
            lastValue = str(rows_df.iat[0, 0])
            logging.info("BQ: last value of column "+column + " is:"+lastValue)
            return lastValue

        def create(self,schema,**kwargs):
            logging.info("creating new table")
            self.table = bigquery.Table(table_ref=self.path, schema=schema)
            if "partitionBy" in kwargs:
                self.table.time_partitioning = bigquery.TimePartitioning(field=kwargs["partitionBy"])
            self.bq_client.create_table(self.table)
            self.schema = self.table.schema

            f = io.StringIO("")
            self.bq_client.schema_to_json(self.schema, f)
            self.schema_dict = bigQuery.convert_schema_to_dict(json.loads(f.getvalue()))

            logging.info("table " + self.path + " created")

        def upload(self, data, config_object,create_nonexisting_table=False,bq_conversion=False,**kwargs):
            input_data_type = type(data)
            total_rows = len(data)
            chunk_size = 20000

            if create_nonexisting_table == True and self.exists == False:
                if "schema" not in list(config_object.keys()) and input_data_type in [dict,list]:
                    schema_dict = utls.dictionary(data).formatting(formatting_type="types_parsing")[0]
                    schema = bigQuery.map_dict_to_schema(schema_dict)
                else:
                    schema = config_object["schema"]

                if "partitionBy" in config_object:
                    self.create(schema=schema,
                                partitionBy=config_object["partitionBy"])
                else:
                    self.create(schema=schema)

            if total_rows > 0:

                if bq_conversion == True:
                    if input_data_type == pandas.core.frame.DataFrame:
                        data = self.pd_convertSchemaToBQ(data)
                    elif input_data_type in [dict,list]:
                        data = utls.dictionary(input=data).formatting(
                                                    formatting_type="bq_conversion",
                                                    schema=self.schema_dict,
                                                    pass_unknown_values=True)

                logging.info("BQ TABLE UPLOAD: set load job configuration")
                job_config = bigquery.LoadJobConfig()


                if "schema" in list(config_object.keys()):
                    job_config.schema = config_object["schema"]
                else:
                    job_config.autodetect = True



                logging.info("BQ TABLE UPLOAD: type of upload: incremental" if "incremental" in list(config_object.keys()) else "BQ TABLE UPLOAD: type of upload: full load")
                if "incremental" in list(config_object.keys()) and self.exists == True:
                    logging.info("     get unique keys values for new rows in source table")
                    logging.info("")

                    uniqueKeys_columnName = config_object["incremental"]["uniqueKey"]
                    if input_data_type == pandas.core.frame.DataFrame:
                        uniqueKeys_values = list(data[uniqueKeys_columnName].astype(str).values)
                        if data[uniqueKeys_columnName].dtype.name in ["string","object"]:
                            uniqueKeys_values = ["'" + i + "'" for i in uniqueKeys_values]
                    elif input_data_type == list:
                        uniqueKeys_values = [str(i[uniqueKeys_columnName]) for i in data]


                    logging.info("     delete rows with this keys from BQ table: "+str(uniqueKeys_values))
                    logging.info("")

                    delete_query = "DELETE FROM `" + self.path + "` WHERE " + config_object["incremental"][
                        "uniqueKey"] + " IN (" + ",".join(uniqueKeys_values) + ")"
                    logging.info("    " + delete_query)
                    job = self.bq_client.query(delete_query)
                    job.result()
                    logging.info("")
                    logging.info("     total rows affected: " + str(job.num_dml_affected_rows))
                else:
                    job_config.write_disposition = "WRITE_APPEND"

                if "partitionBy" in list(config_object.keys()):
                    job_config.time_partitioning = bigquery.TimePartitioning(field=config_object["partitionBy"])

                if "write_disposition" in list(config_object.keys()):
                    job_config.write_disposition = config_object["write_disposition"]

                if "allow_jagged_rows" in list(config_object.keys()):
                    job_config.allow_jagged_rows = config_object["allow_jagged_rows"]

                logging.info("BQ TABLE UPLOAD: final job configuration: "+ str(job_config))
                logging.info("")

                start_row = 0
                end_row = min(chunk_size,total_rows)
                error_row = ""
                logging.info("start upload job into table: " + self.path)

                while (end_row <= total_rows and start_row != end_row) or error_row != "" :
                    chunk_data = data[start_row:end_row]


                    if input_data_type == pandas.core.frame.DataFrame:
                        job_config.source_format = bigquery.SourceFormat.CSV
                        job = self.bq_client.load_table_from_dataframe(dataframe=chunk_data,
                                                                       destination=self.path,
                                                                       job_config=job_config)
                    if input_data_type in [dict,list]:
                        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
                        chunk_data = data[start_row:end_row]

                        job = self.bq_client.load_table_from_json(json_rows=chunk_data,
                                                                  destination=self.path,
                                                                  job_config=job_config)
                    try:
                        job.result()
                        logging.info("chunk upload job successful. number of rows added in total: " + str(end_row))
                        start_row = end_row
                        end_row = min(end_row + chunk_size,total_rows)
                    except Exception as e:
                        error_message=str(e)
                        if "Rows:" in error_message:
                            import io
                            import re
                            error_row=int(re.search("Rows: (\d+);",error_message).group(1))-1
                            error_data = chunk_data[error_row]
                            error_schema=bigQuery.map_dict_to_schema(error_data)
                            f = io.StringIO("")
                            self.bq_client.schema_to_json(error_schema,f)
                            error_schema_dict=self.bq_client.convert_schema_to_dict(json.loads(f.getvalue()))
                            error_schema_dif = [x for x in error_schema_dict if x not in self.schema_dict]


                return logging.info("upload job successful. number of rows added : "+ str(len(data)))
            else:
                return logging.info("no data in source table, upload asserted")

        def pd_convertSchemaToBQ(self,pd_dataframe):
            logging.info("PANDAS TO BQ SCHEMA: starting")

            datatypes_bqTopd = {"STRING": "string",
                                "INTEGER": "Int64",
                                "FLOAT": "float64",
                                "TIMESTAMP": "datetime64",
                                "BOOLEAN": "bool",
                                "BYTES": "object",
                                "DATE": "datetime64",
                                "DATETIME": "datetime64"}
            logging.info("")
            logging.info("     Conversion rules:"+str(datatypes_bqTopd))

            logging.info("     Start checking the columns")
            for i in range(0, len(self.schema)):
                bq_dt = self.schema[i].field_type
                column_name = self.schema[i].name



                pd_dt = str(pd_dataframe.dtypes[i])
                if str.capitalize(datatypes_bqTopd[bq_dt]) not in str.capitalize(pd_dt):
                    try:
                        if pd_dataframe[column_name].dtype == "int64":
                            pd_dataframe[column_name].fillna(value=np.nan,inplace=True)

                        pd_dataframe[column_name] = pd_dataframe[column_name].astype(datatypes_bqTopd[bq_dt])

                        logging.info("     column " + column_name + " converted from type " + pd_dt + " to " + datatypes_bqTopd[bq_dt])
                    except Exception as e:
                        logging.info("PANDAS TO BQ SCHEMA: ERROR")
                        logging.info("Column " + column_name + " not found. Error description" + str(e))
            logging.info("PANDAS TO BQ SCHEMA: SUCESS")
            return pd_dataframe






