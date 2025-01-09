import pytest
import pandas as pd
from utils.sheets_helper import process_transactions, clean_label, format_for_sheets

def test_process_transactions():
    # Setup
    test_transactions = [
        {
            "date": "2024-03-20",
            "libelle": "TEST transaction",
            "montant": 100.0
        }
    ]
    
    # Execute
    df = process_transactions(test_transactions)
    
    # Assert
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['date', 'libelle', 'montant']
    assert df['libelle'].iloc[0] == "TEST TRANSACTION"
    assert df['montant'].iloc[0] == 100.0

def test_clean_label():
    # Test cases
    test_cases = [
        ("Test Transaction!", "TEST TRANSACTION"),
        ("  Multiple   Spaces  ", "MULTIPLE SPACES"),
        ("Special@#$Characters", "SPECIAL CHARACTERS"),
    ]
    
    # Execute & Assert
    for input_text, expected in test_cases:
        assert clean_label(input_text) == expected

def test_format_for_sheets():
    # Setup
    df = pd.DataFrame({
        'date': pd.to_datetime(['2024-03-20']),
        'libelle': ['TEST TRANSACTION'],
        'montant': [100.0]
    })
    
    # Execute
    values = format_for_sheets(df)
    
    # Assert
    assert isinstance(values, list)
    assert len(values) == 1
    assert values[0][0] == '2024-03-20'
    assert values[0][1] == 'TEST TRANSACTION'
    assert values[0][2] == 100.0 

def test_process_transactions_empty():
    # Test avec une liste vide
    df = process_transactions([])
    assert len(df) == 0
    assert list(df.columns) == ['date', 'libelle', 'montant']

def test_process_transactions_invalid_date():
    # Test avec une date invalide
    test_transactions = [{
        "date": "invalid_date",
        "libelle": "TEST",
        "montant": 100.0
    }]
    
    with pytest.raises(Exception) as exc_info:
        process_transactions(test_transactions)
    assert "date" in str(exc_info.value)

def test_clean_label_edge_cases():
    # Test des cas limites pour le nettoyage des libellés
    test_cases = [
        ("", ""),  # Chaîne vide
        ("   ", ""),  # Espaces uniquement
        ("123!@#", "123"),  # Caractères spéciaux uniquement
        ("très lång strîng with àccents", "TRES LANG STRING WITH ACCENTS"),  # Accents
    ]
    
    for input_text, expected in test_cases:
        assert clean_label(input_text) == expected

def test_format_for_sheets_empty():
    # Test avec un DataFrame vide
    df = pd.DataFrame(columns=['date', 'libelle', 'montant'])
    values = format_for_sheets(df)
    assert len(values) == 0 