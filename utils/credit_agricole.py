import boto3
import json
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
from creditagricole_particuliers import Authenticator, Accounts
from utils.config import settings

class CreditAgricoleConfig(BaseModel):
    account_number: str  # Numéro de compte à 11 chiffres (sert aussi d'identifiant)
    password: List[int]  # Code personnel à 6 chiffres
    department: int      # Code département de la caisse régionale

class CreditAgricoleClient:
    @staticmethod
    def get_config():
        try:
            secrets_client = boto3.client('secretsmanager', region_name=settings.AWS_REGION)
            response = secrets_client.get_secret_value(SecretId=settings.CA_CREDENTIALS_SECRET_ID)
            return CreditAgricoleConfig(**json.loads(response['SecretString']))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération des credentials Crédit Agricole: {str(e)}"
            )
    
    @staticmethod
    def get_transactions():
        try:
            config = CreditAgricoleClient.get_config()
            
            session = Authenticator(
                username=config.account_number,
                password=config.password,
                department=config.department
            )
            
            account = Accounts(session=session).search(num=config.account_number)
            operations = account.get_operations()
            
            return [
                {
                    "date": op.date.strftime("%Y-%m-%d"),
                    "libelle": op.libelle,
                    "montant": float(op.montant)
                }
                for op in operations
            ]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération des transactions: {str(e)}"
            ) 