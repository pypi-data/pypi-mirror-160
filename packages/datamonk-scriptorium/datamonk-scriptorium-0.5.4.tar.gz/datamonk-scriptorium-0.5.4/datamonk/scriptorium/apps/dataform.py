import requests
import time
import json
import logging
logger=logging.getLogger(__name__)

class instance():
    def __init__(self,project_id,token):
        self.base_url='https://api.dataform.co/v1/project/'+project_id+'/run'
        self.headers={'Authorization': 'Bearer '+token}

    def run(self,schedule,environment="production"):
        run_create_request = {"environmentName": environment, "scheduleName": schedule}
        response = requests.post(self.base_url, data=json.dumps(run_create_request), headers=self.headers)

        run_url = self.base_url + '/' + response.json()['id']

        status = 'RUNNING'
        while status == 'RUNNING':
            time.sleep(5)
            response = requests.get(run_url, headers=self.headers)
            status = response.json()['status']

        logger.info(response.json())