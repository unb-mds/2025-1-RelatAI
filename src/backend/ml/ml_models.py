import pandas as pd
import numpy as np
import pickle
import os
from datetime import timedelta
import torch
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Implementação otimizada de um modelo baseado em DeepSeek para séries temporais
class DeepSeekTimeSeriesModel:
    def __init__(self, input_size=15, hidden_size=32, output_size=1, num_layers=1, dropout=0.2):
        """
        Modelo otimizado de séries temporais baseado em LSTM
        
        Args:
            input_size: Tamanho da janela de entrada (lookback)
            hidden_size: Dimensão dos estados ocultos da LSTM
            output_size: Número de pontos a prever por vez (geralmente 1)
            num_layers: Número de camadas da LSTM
            dropout: Taxa de dropout (apenas aplicado quando num_layers > 1)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Modelo LSTM com dropout
        dropout_param = dropout if num_layers > 1 else 0
        self.model = torch.nn.LSTM(
            input_size=1, 
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout_param  # Dropout só funciona com múltiplas camadas
        )
        
       # Camadas lineares
        self.linear1 = torch.nn.Linear(hidden_size, hidden_size//2)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(hidden_size//2, output_size)

        # Colocar no dispositivo
        self.model.to(self.device)
        self.linear1.to(self.device)
        self.relu.to(self.device)
        self.linear2.to(self.device)

        # Otimizador com todos os parâmetros
        self.optimizer = torch.optim.Adam(
            list(self.model.parameters()) + 
            list(self.linear1.parameters()) + 
            list(self.linear2.parameters()),
            lr=0.001,
            weight_decay=1e-5  # Regularização L2
        )
        self.loss_fn = torch.nn.MSELoss()
        
        # Para normalização
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def prepare_data(self, series, window_size):
        """Prepara dados para treino ou previsão"""
        X, y = [], []
        for i in range(len(series) - window_size):
            X.append(series[i:i+window_size])
            y.append(series[i+window_size])
        
        return np.array(X), np.array(y)
    
    def fit(self, data, epochs=40, batch_size=64, verbose=False):
        """Treina o modelo com parâmetros otimizados para velocidade"""
        # Normalizar dados
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1)).flatten()
        
        # Preparar conjuntos de treino
        X, y = self.prepare_data(scaled_data, self.input_size)
        X = X.reshape(X.shape[0], X.shape[1], 1)  # Formato (batch, seq_len, features)
        
        # Converter para tensores PyTorch
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
    
        # Treinar o modelo
        for epoch in range(epochs):
            self.model.train()
            
            # Processar em batches maiores para velocidade
            for i in range(0, len(X), batch_size):
                # Criar batch
                x_batch = X_tensor[i:i+batch_size]
                y_batch = y_tensor[i:i+batch_size]
                
                # Forward pass
                self.optimizer.zero_grad()
                output, _ = self.model(x_batch)
                # Use linear1 e linear2 em sequência em vez de self.linear
                output = self.linear1(output[:, -1, :])
                output = self.relu(output)
                output = self.linear2(output)
                
                # Computar perda
                loss = self.loss_fn(output.squeeze(), y_batch)
                
                # Backward pass e otimização
                loss.backward()
                self.optimizer.step()
            
            # Log de progresso reduzido
            if verbose and (epoch+1) % 10 == 0:
                print(f"Época {epoch+1}/{epochs}, Loss: {loss.item():.6f}")
            
        return self
    
    def predict(self, input_data, steps=90):
        """Versão mais rápida com pós-processamento para estabilidade"""
        self.model.eval()
        
        # Normalizar últimos pontos
        last_sequence = input_data[-self.input_size:].reshape(-1, 1)
        last_sequence = self.scaler.transform(last_sequence).flatten()
        current_sequence = torch.FloatTensor(last_sequence.reshape(1, -1, 1)).to(self.device)
        
        predictions = []
        
        # Usar batching para acelerar previsão
        batch_size = min(30, steps)  # Processar em lotes
        batches = (steps + batch_size - 1) // batch_size
        
        for batch in range(batches):
            batch_predictions = []
            steps_in_batch = min(batch_size, steps - batch * batch_size)
            
            # Previsões em uma única passagem para este lote
            with torch.no_grad():
                for _ in range(steps_in_batch):
                    output, _ = self.model(current_sequence)
                    output = self.linear1(output[:, -1, :])
                    output = self.relu(output)
                    output = self.linear2(output)
                    
                    predicted = output.item()
                    batch_predictions.append(predicted)
                    
                    # Atualizar sequência para próxima iteração
                    current_sequence = torch.cat([
                        current_sequence[:, 1:, :], 
                        output.reshape(1, 1, 1)
                    ], dim=1)
            
            predictions.extend(batch_predictions)
        
        # Desnormalizar
        predictions_array = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions_array).flatten()
        
        return predictions

def predict_future_values(historical_data, periods=90, window_size=15, model_type="deepseek"):
    """
    Prevê valores futuros usando modelos de machine learning
    
    Args:
        historical_data: Dados históricos
        periods: Número de períodos a prever
        window_size: Tamanho da janela de lookback
        model_type: Tipo de modelo ("deepseek", "forest" ou "linear")
        
    Returns:
        DataFrame com previsões
    """
    try:
        if not historical_data or len(historical_data) < max(10, window_size + 5):
            return None
        
        # Preparar dados
        df = pd.DataFrame(historical_data)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        
        if df['valor'].dtype == 'object':
            df['valor'] = df['valor'].str.replace(',', '.')
            
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df = df.dropna().sort_values('data')
        
        values = df['valor'].values
        
        # Escolher modelo baseado em desempenho e velocidade
        # Se a série for muito volátil, use RandomForest em vez de DeepSeek
        volatility = np.std(np.diff(values[-30:]))
        mean_value = np.mean(np.abs(values[-30:]))
        volatility_ratio = volatility / mean_value if mean_value > 0 else 0
        
        # Quando a volatilidade é extrema, DeepSeek pode gerar previsões irreais
        if volatility_ratio > 0.15 and model_type == "deepseek":
            print("Série muito volátil. Usando RandomForest para melhor estabilidade.")
            model_type = "forest"
        
        if model_type == "deepseek":
            # Configurações mais rápidas
            model = DeepSeekTimeSeriesModel(
                input_size=window_size,
                hidden_size=32,     # Reduzido para velocidade
                num_layers=1,       # Reduzido para velocidade
                output_size=1,
                dropout=0.1
            )
            
            # Menos épocas = mais rápido
            model.fit(values, epochs=30, batch_size=128, verbose=False)
            
            # Fazer previsão
            predictions = model.predict(values, steps=periods)
            
            # Estabilizar previsão
            last_value = values[-1]
            first_pred = predictions[0]
            
            # Assegurar que a primeira previsão não seja muito diferente do último valor histórico
            if abs(first_pred - last_value) > 0.05 * last_value:
                predictions[0] = last_value * 0.7 + first_pred * 0.3
            
            # Suavizar previsões extremas
            for i in range(1, len(predictions)):
                previous = predictions[i-1]
                current = predictions[i]
                if abs(current - previous) > 0.1 * previous:
                    # Limitar mudanças bruscas
                    direction = 1 if current > previous else -1
                    predictions[i] = previous + direction * 0.05 * previous
            
            # Confiabilidade diminui com o tempo
            confidence_scores = [round(0.95 * np.exp(-0.01 * i), 3) for i in range(periods)]
            
            # Criar datas futuras
            last_date = df['data'].iloc[-1]
            future_dates = [last_date + timedelta(days=i+1) for i in range(periods)]
            
            # Retornar DataFrame
            forecast_df = pd.DataFrame({
                'data': future_dates,
                'valor': predictions,
                'previsto': True,
                'confiabilidade': confidence_scores
            })
            
            return forecast_df
            
        else:
            # Usar implementação anterior para modelos tradicionais
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
                confidence = 0.95 * np.exp(-0.02 * i)  
                confidence_scores.append(round(confidence, 3))
                
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
    
def visualize_forecast(historical_data, forecast_df, title="Previsão", save_path=None):
    """
    Visualiza dados históricos e previsões
    
    Args:
        historical_data: DataFrame com dados históricos
        forecast_df: DataFrame com previsões
        title: Título do gráfico
        save_path: Caminho para salvar o gráfico (opcional)
    """
    plt.figure(figsize=(12, 6))
    
    # Converter para DataFrame se for lista de dicionários
    if isinstance(historical_data, list):
        hist_df = pd.DataFrame(historical_data)
        hist_df['data'] = pd.to_datetime(hist_df['data'], dayfirst=True)
    else:
        hist_df = historical_data
    
    # Plotar dados históricos
    plt.plot(hist_df['data'], hist_df['valor'], color='blue', label='Histórico')
    
    # Plotar previsões
    plt.plot(forecast_df['data'], forecast_df['valor'], color='red', label='Previsão')
    
    # Configurar gráfico (sem plotar intervalos de confiança)
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar se caminho fornecido
    if save_path:
        plt.savefig(save_path)
        
    plt.show()

def evaluate_model(model, X_test, y_test, is_deepseek=False):
    """Avalia o desempenho do modelo"""
    if is_deepseek:
        # Avaliação para modelo DeepSeek
        model.model.eval()
        with torch.no_grad():
            # Preparar dados para previsão
            X_tensor = torch.FloatTensor(X_test.reshape(X_test.shape[0], -1, 1)).to(model.device)
            
            # Fazer previsões (usar linear1 e linear2)
            outputs, _ = model.model(X_tensor)
            outputs = model.linear1(outputs[:, -1, :])
            outputs = model.relu(outputs)
            y_pred = model.linear2(outputs).cpu().numpy().flatten()
    else:
        # Avaliação para modelos sklearn
        y_pred = model.predict(X_test)
    
    # Calcular métricas
    metrics = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'R²': r2_score(y_test, y_pred)
    }
    
    return metrics

def save_model(model, scaler, indicator_name, model_dir=None, is_deepseek=False):
    """Salva o modelo treinado e scaler"""
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'models')
    
    os.makedirs(model_dir, exist_ok=True)
    
    # Salvar o modelo
    model_path = os.path.join(model_dir, f"{indicator_name}_model.pkl")
    
    if is_deepseek:
        # Salvar modelo PyTorch com linear1 e linear2
        torch.save({
            'model_state_dict': model.model.state_dict(),
            'linear1_state_dict': model.linear1.state_dict(),
            'linear2_state_dict': model.linear2.state_dict(),
            'input_size': model.input_size,
            'hidden_size': model.hidden_size,
            'num_layers': model.num_layers,
        }, model_path)
    else:
        # Salvar modelo sklearn
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
    
    # Salvar o scaler
    scaler_path = os.path.join(model_dir, f"{indicator_name}_scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
        
    return model_path

def load_model(indicator_name, model_dir=None, model_type="deepseek"):
    """Carrega modelo e scaler"""
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'models')
    
    model_path = os.path.join(model_dir, f"{indicator_name}_model.pkl")
    scaler_path = os.path.join(model_dir, f"{indicator_name}_scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
    
    # Carregar scaler
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    
    if model_type == "deepseek":
        # Carregar modelo DeepSeek
        checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        
        # Recriar modelo
        model = DeepSeekTimeSeriesModel(
            input_size=checkpoint['input_size'],
            hidden_size=checkpoint['hidden_size'],
            num_layers=checkpoint['num_layers']
        )
        
        # Carregar pesos
        model.model.load_state_dict(checkpoint['model_state_dict'])
        # Adaptar para os novos nomes linear1 e linear2
        if 'linear1_state_dict' in checkpoint:
            model.linear1.load_state_dict(checkpoint['linear1_state_dict'])
            model.linear2.load_state_dict(checkpoint['linear2_state_dict'])
        elif 'linear_state_dict' in checkpoint:
            # Compatibilidade com modelos antigos
            print("Modelo antigo detectado. Convertendo...")
        model.scaler = scaler
    else:
        # Carregar modelo sklearn
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    
    return model, scaler