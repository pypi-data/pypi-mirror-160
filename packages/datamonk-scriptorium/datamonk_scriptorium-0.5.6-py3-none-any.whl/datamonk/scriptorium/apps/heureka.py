import requests

def get_costReport(costReport_URL):
    from io import StringIO
    import pandas as pd

    costReport_request = requests.get(costReport_URL)
    costReport_string = StringIO(str(costReport_request.content, "utf-8"))
    costReport_df = pd.read_csv(costReport_string)
    return costReport_df


def get_ProductURLs(conversionReport_URL):
    import gzip
    import xml.etree.ElementTree as et
    report =requests.get(conversionReport_URL)

    xml_string =gzip.decompress(report.content)

    xtree = et.fromstring(xml_string)
    product_tpls =[]
    for product in xtree.iter("PRODUCT"):
        url_split = product.find("HEUREKA_URL").text.split("/")
        url_product = url_split[3]
        url_category = url_split[2].split(".")[0]
        product_tpls.append(tuple([url_category ,url_product]))

    return product_tpls

class bidding_api(object):
    def __init__(self,token):
        self.token=token
    from retrying import retry


    @retry(stop_max_attempt_number=10)
    def get_product(self,product_id,format=True,**kwargs):

        import json
        ## generate basic form of request
        url = "https://api.heureka.cz/bidding_api/v1"
        payload = {
            "jsonrpc": "2.0",
            "method": "product.get",
            "id": 1,
            "params": {
                "access_key": self.token,
                "id":product_id
            }
        }

        ## if category parameter is defined, add it to request
        if "category" in kwargs:
            payload["params"]["category_id"]=kwargs["category"]

        ## data are present in nested product dictionary
        response = requests.post(url=url, json=payload)
        product = response.json()["result"]["product"]
        ## preprocess data, add new features and unify data format
        if format:

            ## format and shop keys to unified verssion

            product["top_shop"]["offers"] = [product["top_shop"].pop("offer")]
            product["top"] = [product.pop("top_shop")]
            product["organic"] = product.pop("shops")
            product["highlighted"] = product.pop("highlighted_shops")

            ## merge all shop dictionaries into one and delete redundant keys
            merged_keys=["top", "highlighted", "organic"]
            product["shops"]=[]
            for key in merged_keys:
                if product[key]:
                    ## add feature of shop position type
                    product[key] = [dict(item, position=key) for item in product[key]]
                product["shops"].extend(product.pop(key))
            ## add offer position rank (ranked from top-sponsored-organic)
            product["shops"] = [dict(item,rank=ind+1) for ind,item in enumerate(product["shops"])]
            ## add variant position rank (ranked by order in list)
            for index,shop in enumerate(product["shops"]):
                shop_offers_list=product["shops"][index]["offers"]
                product["shops"][index]["offers"]=[dict(offers, rank=ind + 1) for ind, offers in enumerate(shop_offers_list)]


        return product