import os.path
import pandas as pd

from __future__ import print_function

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
service = build('sheets', 'v4', credentials=creds)

#Call the sheets API
sheet = service.spreadsheets()

#loading the content of the google sheet and converting spreadsheet into dict of dataframes

sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()

#transforming the content into a dictionary of pandas dataframe
df_dict = {}
properties = sheet_metadata.get('sheets')

for item in properties:
    table = item.get('properties').get('title')
    df_dict[table] = pd.DataFrame()

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=table + '!A1:J').execute()
    header = result.get('values',[])[0]
    values = result.get('values',[])[1:]
    if not values:
        print('No values found')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                if col_id < len(row):
                    column_data.append(row[col_id])
                else:
                    column_data.append('')
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df_dict[table] = pd.concat(all_data, axis=1)

#creating a mapping between the tables and django model class

tables = {}
for table,df in df_dict.items():
    tables[table] = {}
    for i in range(0, df.shape[0]):
        attr = {}
        if df['MAX LENGTH'][i] != '':
            attr['max_length'] = df['MAX LENGTH'][i]
        if df['KEY'][i] == 'primary key':
            attr['primary_key'] = 'True'
        tables[table][df['ATTRIBUTES'][i]] = [df['DATA TYPE'][i],attr]
tables

#create the content of the model.py script
def get_type(attr_type):
    if isinstance(attr_type, list):
        attr = attr_type[0] + 'Field('
        for k,v in attr_type[1].items():
            attr = attr + k + '=' + v + ','
        attr = attr[:-1]
        return attr + (')\n')
    else:
        return attr_type + 'field()\n'

script = 'from django.db import models\n'
#build model class for each item in the table
for model,attributes in tables.items():
    script = script + "class" + model + "(models.Model):\n"
    for attr_name,attr_type in attributes.items():
        script = script + '\t' + attr_name + '=models.' + get_type(attr_type)
#save result in models.py
root = 'core/load_googlesheet/'
file_name = root + 'models.py'
with open(file_name, "w") as py_file:
    py_file.write(script)