import requests
import pandas as pd
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000"  # Ajuste conforme seu ambiente

def predict_future_values(historical_data, periods=90, window_size=15, model_type="deepseek"):
    try:
        # Preparar dados para a requisição
        payload = {
            "historical_data": historical_data,
            "periods": periods,
            "window_size": window_size,
            "model_type": model_type
        }
        
        # Fazer requisição para o backend
        response = requests.post(
            f"{API_BASE_URL}/predict/{model_type}",
            json=payload
        )
        
        if response.status_code != 200:
            print(f"Erro na API: {response.status_code} - {response.text}")
            return None
            
        # Processar resultado
        data = response.json()
        if not data:
            return None
            
        # Converter para DataFrame
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        
        return df
        
    except Exception as e:
        print(f"Erro ao fazer previsão: {str(e)}")
        return None