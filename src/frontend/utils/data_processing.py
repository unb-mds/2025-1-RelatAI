import pandas as pd
import numpy as np

def process_api_data(data):

    if not data:
        return None
    
    df = pd.DataFrame(data)
    
    df['data'] = pd.to_datetime(df['data'], dayfirst=True) 
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')    
    df = df.dropna()
    df = df.sort_values('data')
    
    return df

def calculate_statistics(df):
    if df is None or df.empty:
        return None
    
    stats = {
        'média': df['valor'].mean(),
        'mediana': df['valor'].median(),
        'min': df['valor'].min(),
        'max': df['valor'].max(),
        'desvio_padrão': df['valor'].std(),
        'variação_percentual': ((df['valor'].iloc[-1] / df['valor'].iloc[0]) - 1) * 100 if len(df) > 1 else 0
    }
    
    return stats

def prepare_data_for_ml(df, window_size=5):
    if df is None or df.empty or len(df) <= window_size:
        return None, None
    
    values = df['valor'].values
    
    X, y = [], []
    for i in range(len(values) - window_size):
        X.append(values[i:i + window_size])
        y.append(values[i + window_size])
    
    return np.array(X), np.array(y)