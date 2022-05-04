from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive'
]

#The ID and range of a sample spreadsheet
SAMPLE_SPREADSHEET_ID = '1HkUSpRdMtYKXI3RxNz9tz5jz1Pa5HpuS'
SAMPLE_RANGE_NAME = 'Employee data!A1:J'

creds = None
#The file token.json stores the users access and refresh tokens,it's created
#automatically when the authosization flow completes for the first time
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json',SCOPES)
#if there are no (valid) credentials available, let the user log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',SCOPES
        )
        creds = flow.run_local_server(port=0)
        #Saving the credentials for the next run
        with open('token.json','w') as token:
            token.write(creds.to_json())
