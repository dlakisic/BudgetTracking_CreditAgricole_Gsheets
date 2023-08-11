import os
from dotenv import load_dotenv
from datetime import datetime

from creditagricole_particuliers import Accounts
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv('.env')

# Access Google Sheets API to interact with the right worksheet
scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name('path to service_account.json',scope)

client = gspread.authorize(creds)

sheet = client.open('spreadsheet_name').worksheet("worksheet_name")

# Define start and end dates for data retrieval
date_start = datetime.today().strftime('%Y-%m-%d')
date_stop = datetime.today().strftime('%Y-%m-%d')

# Client authentication
session = Authenticator(username=os.getenv('USERNAME'),
                        password=os.getenv('PASSWORD'),
						region=os.getenv('DEPARTMENT'))

# Retrieve operations based on date range
operations = Operations(session=session,
                        date_start=date_start,
                        date_stop=date_stop)

# Iterate, format date, and send to GSheet
for index, value in enumerate(operations.list):
    date_obj = datetime.strptime(value['dateOperation'], '%b %d, %Y, %H:%M:%S %p')
    date_str = date_obj.strftime('%m/%y')
    date_op = date_obj.strftime('%d/%m/%Y')
    sheet.append_row([date_str,value['libelleOperation'],value['montant'],date_op])
