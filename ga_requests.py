from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import pandas as pd


#Google Analytics API v4

"""

Input filepath when instantiating class

Input view id when instantiating class

"""

class GA_Reporting:
    def __init__(self, OAuth, view_number):

        self.credentials_file = OAuth
        self.view = view_number

        #report request framework
        self.body = \
        {
            'reportRequests': [
                {
                    'viewId': self.view,
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:country'}]
                }
            ]
        }


    def initialize_analyticsreporting_v2(self):
        SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

        #remeber to use the json generated when you create the service account credentials.
        KEY_FILE_LOCATION = self.credentials_file

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
          KEY_FILE_LOCATION, SCOPES)

        # Build the service object.
        analytics = build('analytics', 'v4', credentials=credentials)
        return analytics

    #modifying report requests
    def mod_date(self):

        self.start_date = raw_input("enter a start date:  ")

            #add a function to ensure proper date format

        self.end_date = raw_input("enter a end date:   ")

            #add a function to ensure proper date format

        for report in self.body['reportRequests']:
            report['dateRanges'][0]["startDate"] = self.start_date
            report['dateRanges'][0]["endDate"] = self.end_date



    #requesting reports
    def get_report(self):

        #generate authentication
        analytics = self.initialize_analyticsreporting_v2()

        return analytics.reports().batchGet(self.body).execute()

    #formatting reports into pandas dataframes