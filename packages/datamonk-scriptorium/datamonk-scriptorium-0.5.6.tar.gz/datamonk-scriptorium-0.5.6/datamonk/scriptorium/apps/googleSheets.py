import os
import pygsheets

class instance():
    def __init__(self,**kwargs):
        if "env_object" in kwargs:
            self.client = pygsheets.authorize(service_account_env_var=kwargs["env_object"])
        else:
            self.client = pygsheets.authorize(service_account_file=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        self.spreadsheets = self.client.spreadsheet_titles()
        if "spreadsheet_name" in kwargs:
            self.spreadsheet=self.client.open(kwargs["spreadsheet_name"])






