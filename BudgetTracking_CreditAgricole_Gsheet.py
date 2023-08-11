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

# Définition de la date de début et fin à récupérer
date_start = datetime.today().strftime('%Y-%m-%d')
date_stop = datetime.today().strftime('%Y-%m-%d')

# Authentification du client 
session = Authenticator(username=os.getenv('USERNAME'),
                        password=os.getenv('PASSWORD'),
						region=os.getenv('DEPARTMENT'))

# Récupération des opérations en fonction de la date
operations = Operations(session=session,
                        date_start=date_start,
                        date_stop=date_stop)

# Iteration formatage de la date + Envoi sur GSheet
for index, value in enumerate(operations.list):
    date_obj = datetime.strptime(value['dateOperation'], '%b %d, %Y, %H:%M:%S %p')
    date_str = date_obj.strftime('%m/%y')
    date_op = date_obj.strftime('%d/%m/%Y')
    sheet.append_row([date_str,value['libelleOperation'],value['montant'],date_op])