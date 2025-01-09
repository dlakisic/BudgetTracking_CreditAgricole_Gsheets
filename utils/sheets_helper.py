import pandas as pd
from typing import List, Dict
from datetime import datetime
import re

def process_transactions(transactions: List[Dict]) -> pd.DataFrame:
    """
    Traite les transactions et retourne un DataFrame formaté
    """
    df = pd.DataFrame(transactions)
    
    # Nettoyage et formatage des colonnes
    df['date'] = pd.to_datetime(df['date'])
    df['montant'] = df['montant'].astype(float)
    
    # Nettoyage des libellés
    df['libelle'] = df['libelle'].apply(clean_label)
    
    # Réorganisation des colonnes
    columns = ['date', 'libelle', 'montant']
    df = df[columns]
    
    return df

def clean_label(label: str) -> str:
    """
    Nettoie et standardise les libellés
    """
    # Suppression des caractères spéciaux
    label = re.sub(r'[^\w\s]', ' ', label)
    # Suppression des espaces multiples
    label = re.sub(r'\s+', ' ', label)
    return label.strip().upper()

def format_for_sheets(df: pd.DataFrame) -> List[List]:
    """
    Formate le DataFrame pour l'insertion dans Google Sheets
    """
    # Formatage des dates pour Google Sheets
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Formatage des montants avec 2 décimales
    df['montant'] = df['montant'].round(2)
    
    return df.values.tolist() 