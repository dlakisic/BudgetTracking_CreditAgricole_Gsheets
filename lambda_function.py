from fastapi import FastAPI, HTTPException
from mangum import Mangum
from utils.credit_agricole import CreditAgricoleClient
from utils.google_sheets import GoogleSheetsClient
from utils.sheets_helper import process_transactions, format_for_sheets
from utils.logger import setup_logger

app = FastAPI()

logger = setup_logger()

@app.post("/fetch-transactions")
async def fetch_transactions():
    try:
        logger.info("Début de la récupération des transactions")
        transactions = CreditAgricoleClient.get_transactions()
        logger.info(f"Récupération de {len(transactions)} transactions")
        
        logger.info("Traitement des transactions")
        df = process_transactions(transactions)
        values = format_for_sheets(df)
        
        logger.info("Ajout dans Google Sheets")
        sheets_client = GoogleSheetsClient()
        rows_added = sheets_client.append_transactions(values)
        
        logger.info(f"Ajout réussi de {rows_added} transactions")
        return {
            "status": "success",
            "message": f"Added {rows_added} transactions"
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

handler = Mangum(app) 