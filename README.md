# BudgetTracking_CreditAgricole_Gsheet

Here's the first Python project that I did back in 2020. This repository houses a Python script aimed at collecting diverse banking transactions from an account using the third-party package python-creditagricole-particuliers, developed by <a href="https://github.com/dmachard/python-creditagricole-particuliers" target="_blank">dmachard</a>. The acquired transaction data is then seamlessly integrated into a designated Google Sheets worksheet, which acts as an efficient budget tracking tool.

## Technologies Used

• **python-creditagricole-particuliers**: A Python package created by dmachard, which facilitates access to Credit Agricole account details and transaction records.

• **gspread**: A package that streamlines interactions with Google Sheets, enabling the addition of transaction information into a specified worksheet.

• **AWS Lambda & FastAPI**: The project is hosted on AWS Lambda using FastAPI for the API endpoints.

• **AWS Secrets Manager**: Securely stores credentials for both Google and Crédit Agricole.

• **Google Sheets**: Acts as the database for storing and analyzing transactions. Check out the <a href="https://
docs.google.com/spreadsheets/d/1NvhKyCqQK515gzzyhcQUO0TfHJLnYhUB1hptQ-sZAT0/edit?usp=sharing" target="_blank">Google 
Sheets Template</a>.

## Prerequisites

- Python 3.9+
- AWS CLI configured
- Serverless Framework
- Google Cloud account with Sheets API enabled
- Crédit Agricole online banking account

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS Secrets Manager:

   a. Create `google_credentials` secret:
   ```json
   {
     "type": "service_account",
     "project_id": "your-project",
     "private_key_id": "...",
     "private_key": "...",
     "client_email": "...",
     "client_id": "..."
   }
   ```

   b. Create `credit_agricole_credentials` secret:
   ```json
   {
     "username": "your_id",
     "password": [1, 2, 3, 4, 5, 6],
     "department": 999,
     "account_number": "account_to_track"
   }
   ```

3. Update `serverless.yml` with your configuration:
   ```yaml
   environment:
     SPREADSHEET_ID: 'your_spreadsheet_id'
     SHEET_NAME: 'Transactions'
   ```

## Deployment

Deploy to AWS Lambda:
```bash
serverless deploy
```

## Usage

The service exposes a POST endpoint to fetch transactions:
```bash
curl -X POST https://your-api.execute-api.eu-west-1.amazonaws.com/dev/fetch-transactions
```

You can also set up an EventBridge rule to trigger this endpoint daily.

## Project Structure

```
.
├── README.md                  # Documentation
├── lambda_function.py         # Lambda entry point with FastAPI
├── requirements.txt           # Python dependencies
├── serverless.yml            # Serverless Framework configuration
└── utils/                    # Utility modules
    ├── __init__.py
    ├── config.py             # Global settings and constants
    ├── credit_agricole.py    # Credit Agricole API client
    ├── google_sheets.py      # Google Sheets client
    ├── logger.py             # Logging configuration
    └── sheets_helper.py      # Data processing utilities
```

Key components:
- `lambda_function.py`: Main FastAPI application and Lambda handler
- `utils/config.py`: Configuration settings for AWS and Google services
- `utils/credit_agricole.py`: Client for fetching bank transactions
- `utils/google_sheets.py`: Client for interacting with Google Sheets
- `utils/sheets_helper.py`: Functions for data processing and formatting
- `utils/logger.py`: CloudWatch logging setup

## Logging

All operations are logged to CloudWatch Logs, including:
- Transaction fetching start/end
- Number of transactions processed
- Any errors that occur

## Security

- All credentials are stored in AWS Secrets Manager
- IAM roles control access to secrets
- No local credential storage
- Secure logging in CloudWatch

## Limitations

- Depends on Crédit Agricole API availability
- Subject to Google Sheets API quotas
- Fetches last 30 transactions by default

Please ensure all credentials, paths, and environment variables are properly configured for your environment before deployment.