import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
from datetime import timedelta

def predict_future_values(historical_data, periods=90, window_size=5, model_type="forest"):

    try:
        if not historical_data or len(historical_data) < 10:
            return None
        
        # Preparar dados
        df = pd.DataFrame(historical_data)
        
        # Correção para formato de data brasileiro
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        
        # Converter valores para numéricos
        if df['valor'].dtype == 'object':
            df['valor'] = df['valor'].str.replace(',', '.')
            
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df = df.dropna().sort_values('data')
        
        # Normalizar dados para melhorar previsão
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df[['valor']].values)
        
        # Usar janela deslizante para prever próximo valor
        X, y = [], []
        
        for i in range(window_size, len(scaled_data)):
            X.append(scaled_data[i-window_size:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        
        # Treinar modelo
        if model_type == "linear":
            model = LinearRegression()
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        model.fit(X, y)
        
        # Preparar dados para previsão
        last_window = scaled_data[-window_size:].reshape(-1)
        
        # Fazer previsões
        predictions = []
        confidence_scores = []
        current_batch = last_window.copy()
        
        for i in range(periods):
            # Prever próximo valor
            current_batch_reshaped = current_batch.reshape(1, -1)
            predicted = model.predict(current_batch_reshaped)[0]
            predictions.append(predicted)
            
            # Calcular confiabilidade (decaimento exponencial)
            # Começa com 0.95 (95%) e diminui gradualmente
            confidence = 0.95 * np.exp(-0.02 * i)  
            confidence_scores.append(round(confidence, 3))  # Arredondar para 3 casas decimais
            
            # Atualizar batch para próxima previsão
            current_batch = np.append(current_batch[1:], predicted)
        
        # Inverter normalização
        predictions_array = np.array(predictions).reshape(-1, 1)
        inverse_predictions = scaler.inverse_transform(np.hstack([predictions_array, np.zeros_like(predictions_array)]))[:, 0]
        
        # Criar datas futuras
        last_date = df['data'].iloc[-1]
        future_dates = [last_date + timedelta(days=i+1) for i in range(periods)]
        
        # Retornar como DataFrame com coluna de confiabilidade
        forecast_df = pd.DataFrame({
            'data': future_dates,
            'valor': inverse_predictions,
            'previsto': True,
            'confiabilidade': confidence_scores
        })
        
        return forecast_df
        
    except Exception as e:
        import traceback
        print(f"Erro ao gerar previsões: {str(e)}")
        print(traceback.format_exc())
        return None

def evaluate_model(model, X_test, y_test):
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    
    # Calcular métricas
    metrics = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'R²': r2_score(y_test, y_pred)
    }
    
    return metrics

def save_model(model, scaler, indicator_name, model_dir=None):
 
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'back', 'ipea', 'financeiro', 'ml', 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    # Salvar o modelo
    model_path = os.path.join(model_dir, f"{indicator_name}_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    # Salvar o scaler
    scaler_path = os.path.join(model_dir, f"{indicator_name}_scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
        
    return model_path

def load_model(indicator_name, model_dir=None):
    
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'back', 'ipea', 'financeiro', 'mL', 'models')
    
    model_path = os.path.join(model_dir, f"{indicator_name}_model.pkl")
    scaler_path = os.path.join(model_dir, f"{indicator_name}_scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
    
    # Carregar modelo
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Carregar scaler
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    
    return model, scaler