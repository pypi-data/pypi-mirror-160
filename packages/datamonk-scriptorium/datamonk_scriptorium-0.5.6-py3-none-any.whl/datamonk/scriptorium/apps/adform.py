

#pip install dagmar_adform_api_wrapper
from dagmar_adform_api_wrapper import AdformApi

ADFORM_CLIENT_ID = "ENTER CLIENTID HERE"
ADFORM_CLIENT_SECRET = 'ENTER CLIENT SECRET HERE'

adform_api = AdformApi(ADFORM_CLIENT_ID
                       , ADFORM_CLIENT_SECRET
                       ,scope_list=["buyer.stats"])


post_parameters={"dimensions": ["date",
                                "client",
                                "campaign"
                                ],
  "metrics": [
    {
      "metric": "impressions",
      "specs": {
        "adUniqueness": "campaignUnique"
      }
    },
    {
      "metric": "clicks",
      "specs": {
        "adUniqueness": "campaignUnique"
      }
    }
  ],
  "filter": {
    "date": {
      "from": "2020-12-08T19:10:11.4247904Z",
      "to": "2020-12-08T19:10:11.4247936Z"
    }
  },
  "paging": {
    "offset": 0,
    "limit": 3000
  },
  "includeRowCount": True,
  "includeTotals": True,
  "sort": [
    {
      "dimension": "date",
      "direction": "desc"
    },
    {
      "metric": "impressions",
      "specs": {
        "adUniqueness": "campaignUnique"
      },
      "direction": "asc"
    }
  ]
}

response_post=adform_api.post('/buyer/stats/data',payload=post_parameters)


response_get=adform_api.get(response_post.headers["Location"][3:])
print(response_get.json())