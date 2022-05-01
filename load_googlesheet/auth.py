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
