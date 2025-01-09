import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from utils.google_sheets import GoogleSheetsClient

@pytest.fixture
def mock_boto3():
    with patch('boto3.client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_gspread():
    with patch('gspread.authorize') as mock:
        yield mock

def test_get_credentials_success(mock_boto3):
    # Setup
    mock_response = {
        'SecretString': '{"type": "service_account", "project_id": "test"}'
    }
    mock_boto3.return_value.get_secret_value.return_value = mock_response
    
    # Execute
    with patch('oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_dict') as mock_creds:
        GoogleSheetsClient.get_credentials()
        
        # Assert
        mock_creds.assert_called_once()

def test_get_credentials_error(mock_boto3):
    # Setup
    mock_boto3.return_value.get_secret_value.side_effect = Exception("Credentials not found")
    
    # Execute & Assert
    with pytest.raises(HTTPException) as exc_info:
        GoogleSheetsClient.get_credentials()
    assert exc_info.value.status_code == 500
    assert "Credentials not found" in str(exc_info.value.detail)

def test_append_transactions_success(mock_gspread):
    # Setup
    mock_worksheet = Mock()
    mock_spreadsheet = Mock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_gspread.return_value.open_by_key.return_value = mock_spreadsheet
    
    client = GoogleSheetsClient()
    test_values = [["2024-03-20", "TEST", 100.0]]
    
    with patch.dict('os.environ', {'SPREADSHEET_ID': 'test_id', 'SHEET_NAME': 'test_sheet'}):
        # Execute
        result = client.append_transactions(test_values)
        
        # Assert
        assert result == 1
        mock_worksheet.append_rows.assert_called_once_with(test_values)

def test_append_transactions_missing_env():
    # Setup
    client = GoogleSheetsClient()
    test_values = [["2024-03-20", "TEST", 100.0]]
    
    # Execute & Assert
    with pytest.raises(HTTPException) as exc_info:
        client.append_transactions(test_values)
    assert "SPREADSHEET_ID et SHEET_NAME doivent être configurés" in str(exc_info.value.detail) 

def test_append_transactions_api_error(mock_gspread):
    # Setup
    mock_gspread.return_value.open_by_key.side_effect = Exception("API Error")
    client = GoogleSheetsClient()
    test_values = [["2024-03-20", "TEST", 100.0]]
    
    with patch.dict('os.environ', {'SPREADSHEET_ID': 'test_id', 'SHEET_NAME': 'test_sheet'}):
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            client.append_transactions(test_values)
        assert "API Error" in str(exc_info.value.detail)

def test_get_client_error(mock_boto3):
    # Setup
    mock_boto3.return_value.get_secret_value.return_value = {
        'SecretString': '{"type": "service_account", "project_id": "test"}'
    }
    
    with patch('gspread.authorize') as mock_authorize:
        mock_authorize.side_effect = Exception("Authorization failed")
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            GoogleSheetsClient.get_client()
        assert "Authorization failed" in str(exc_info.value.detail) 