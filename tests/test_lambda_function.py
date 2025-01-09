import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from lambda_function import app

client = TestClient(app)

@pytest.fixture
def mock_ca_client():
    with patch('utils.credit_agricole.CreditAgricoleClient') as mock:
        yield mock

@pytest.fixture
def mock_sheets_client():
    with patch('utils.google_sheets.GoogleSheetsClient') as mock:
        yield mock

def test_fetch_transactions_success(mock_ca_client, mock_sheets_client):
    # Setup
    mock_transactions = [
        {"date": "2024-03-20", "libelle": "TEST", "montant": 100.0}
    ]
    mock_ca_client.get_transactions.return_value = mock_transactions
    mock_sheets_client.return_value.append_transactions.return_value = 1
    
    # Execute
    response = client.post("/fetch-transactions")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Added 1 transactions"
    }

def test_fetch_transactions_ca_error(mock_ca_client):
    # Setup
    mock_ca_client.get_transactions.side_effect = Exception("API Error")
    
    # Execute
    response = client.post("/fetch-transactions")
    
    # Assert
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"] 

def test_fetch_transactions_sheets_error(mock_ca_client, mock_sheets_client):
    # Setup
    mock_transactions = [
        {"date": "2024-03-20", "libelle": "TEST", "montant": 100.0}
    ]
    mock_ca_client.get_transactions.return_value = mock_transactions
    mock_sheets_client.return_value.append_transactions.side_effect = Exception("Sheets API Error")
    
    # Execute
    response = client.post("/fetch-transactions")
    
    # Assert
    assert response.status_code == 500
    assert "Sheets API Error" in response.json()["detail"]

def test_fetch_transactions_empty(mock_ca_client, mock_sheets_client):
    # Setup
    mock_ca_client.get_transactions.return_value = []
    mock_sheets_client.return_value.append_transactions.return_value = 0
    
    # Execute
    response = client.post("/fetch-transactions")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Added 0 transactions"
    }

@pytest.mark.asyncio
async def test_fetch_transactions_timeout(mock_ca_client):
    # Setup
    mock_ca_client.get_transactions.side_effect = TimeoutError("Connection timeout")
    
    # Execute
    response = client.post("/fetch-transactions")
    
    # Assert
    assert response.status_code == 500
    assert "Connection timeout" in response.json()["detail"] 