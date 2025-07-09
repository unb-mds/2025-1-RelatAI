import pytest
import sys
import os
import pandas as pd
from ml.ml_models import predict_future_values

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_predict_future_values_basic():
    data = [
        {"data": "01/01/2023", "valor": 10},
        {"data": "02/01/2023", "valor": 12},
        {"data": "03/01/2023", "valor": 11},
        {"data": "04/01/2023", "valor": 13},
        {"data": "05/01/2023", "valor": 14},
        {"data": "06/01/2023", "valor": 15},
        {"data": "07/01/2023", "valor": 16},
        {"data": "08/01/2023", "valor": 18},
        {"data": "09/01/2023", "valor": 17},
        {"data": "10/01/2023", "valor": 19},
        {"data": "11/01/2023", "valor": 20},
        {"data": "12/01/2023", "valor": 21},
        {"data": "13/01/2023", "valor": 22},
        {"data": "14/01/2023", "valor": 23},
        {"data": "15/01/2023", "valor": 24},
        {"data": "16/01/2023", "valor": 25},
    ]
    
    periods = 5
    df = pd.DataFrame(data)

    forecast_df = predict_future_values(df, periods=periods, window_size=15, model_type="deepseek")

    assert forecast_df is None
