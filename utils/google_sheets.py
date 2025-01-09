import gspread
from oauth2client.service_account import ServiceAccountCredentials
import boto3
import json
from fastapi import HTTPException
import os
from typing import List
from utils.config import settings

class GoogleSheetsClient:
    def __init__(self):
        self.client = self.get_client()
    
    @staticmethod
    def get_credentials():
        try:
            secrets_client = boto3.client('secretsmanager', region_name=settings.AWS_REGION)
            response = secrets_client.get_secret_value(SecretId=settings.GOOGLE_CREDENTIALS_SECRET_ID)
            credentials = json.loads(response['SecretString'])
            return ServiceAccountCredentials.from_json_keyfile_dict(
                credentials,
                settings.GOOGLE_SCOPES
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération des credentials Google: {str(e)}"
            )
    
    @staticmethod
    def get_client():
        try:
            credentials = GoogleSheetsClient.get_credentials()
            return gspread.authorize(credentials)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la connexion à Google Sheets: {str(e)}"
            )
    
    def append_transactions(self, values: List[List]):
        try:
            spreadsheet_id = os.environ.get('SPREADSHEET_ID')
            sheet_name = os.environ.get('SHEET_NAME')
            
            if not spreadsheet_id or not sheet_name:
                raise ValueError("SPREADSHEET_ID et SHEET_NAME doivent être configurés")
            
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.append_rows(values)
            
            return len(values)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'ajout des transactions: {str(e)}"
            ) 