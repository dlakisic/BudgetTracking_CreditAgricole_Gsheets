import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from utils.credit_agricole import CreditAgricoleClient, CreditAgricoleConfig

@pytest.fixture
def mock_boto3():
    with patch('boto3.client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_authenticator():
    with patch('creditagricole_particuliers.Authenticator') as mock:
        yield mock

@pytest.fixture
def mock_accounts():
    with patch('creditagricole_particuliers.Accounts') as mock:
        yield mock

def test_get_config_success(mock_boto3):
    # Setup
    mock_response = {
        'SecretString': '{"username": "test", "password": [1,2,3,4,5,6], "department": 999, "account_number": "123"}'
    }
    mock_boto3.return_value.get_secret_value.return_value = mock_response
    
    # Execute
    config = CreditAgricoleClient.get_config()
    
    # Assert
    assert isinstance(config, CreditAgricoleConfig)
    assert config.username == "test"
    assert config.password == [1,2,3,4,5,6]
    assert config.department == 999
    assert config.account_number == "123"

def test_get_config_error(mock_boto3):
    # Setup
    mock_boto3.return_value.get_secret_value.side_effect = Exception("Secret not found")
    
    # Execute & Assert
    with pytest.raises(HTTPException) as exc_info:
        CreditAgricoleClient.get_config()
    assert exc_info.value.status_code == 500
    assert "Secret not found" in str(exc_info.value.detail)

def test_get_transactions_success(mock_boto3, mock_authenticator, mock_accounts):
    # Setup
    mock_response = {
        'SecretString': '{"username": "test", "password": [1,2,3,4,5,6], "department": 999, "account_number": "123"}'
    }
    mock_boto3.return_value.get_secret_value.return_value = mock_response
    
    mock_operation = Mock()
    mock_operation.date.strftime.return_value = "2024-03-20"
    mock_operation.libelle = "TEST TRANSACTION"
    mock_operation.montant = 100.0
    
    mock_accounts.return_value.search.return_value.get_operations.return_value = [mock_operation]
    
    # Execute
    transactions = CreditAgricoleClient.get_transactions()
    
    # Assert
    assert len(transactions) == 1
    assert transactions[0]["date"] == "2024-03-20"
    assert transactions[0]["libelle"] == "TEST TRANSACTION"
    assert transactions[0]["montant"] == 100.0 

def test_get_transactions_error(mock_boto3, mock_authenticator, mock_accounts):
    # Setup
    mock_boto3.return_value.get_secret_value.return_value = {
        'SecretString': '{"username": "test", "password": [1,2,3,4,5,6], "department": 999, "account_number": "123"}'
    }
    
    # Simuler une erreur lors de la récupération des opérations
    mock_accounts.return_value.search.return_value.get_operations.side_effect = Exception("API Error")
    
    # Execute & Assert
    with pytest.raises(HTTPException) as exc_info:
        CreditAgricoleClient.get_transactions()
    assert exc_info.value.status_code == 500
    assert "API Error" in str(exc_info.value.detail) 