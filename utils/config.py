from typing import List

class Settings:
    # AWS Secrets Manager IDs
    GOOGLE_CREDENTIALS_SECRET_ID: str = "google_credentials"
    CA_CREDENTIALS_SECRET_ID: str = "credit_agricole_credentials"
    AWS_REGION: str = "eu-west-1"
    
    # Google Sheets scopes
    GOOGLE_SCOPES: List[str] = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

settings = Settings() 