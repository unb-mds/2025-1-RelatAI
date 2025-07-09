import requests
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Configurar logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://two025-1-relatai.onrender.com"

def predict_future_values(historical_data, periods=90, window_size=15, model_type="deepseek", indicator_name="selic"):
    try:
        # Verificar se temos dados históricos
        if not historical_data or len(historical_data) < 2:
            logger.error(f"Dados históricos insuficientes para {indicator_name}")
            return None
        
        # Verificar se é um indicador trimestral
        quarterly_indicators = ["pib"]
        
        if indicator_name.lower() in quarterly_indicators:
            logger.info(f"Usando previsão trimestral para {indicator_name}")
            return predict_quarterly_indicator(historical_data, periods, indicator_name)
            
        # Para outros indicadores, seguir o fluxo normal
        # Preparar dados para a requisição
        payload = {
            "historical_data": historical_data,
            "periods": periods,
            "window_size": window_size,
            "model_type": model_type
        }
        
        logger.info(f"Solicitando previsão para {indicator_name}, {periods} períodos")
        
        # URL CORRETA: /predict/{indicator_name}
        response = requests.post(
            f"{API_BASE_URL}/predict/{indicator_name}",
            json=payload
        )
        
        if response.status_code != 200:
            logger.error(f"Erro na API: {response.status_code} - {response.text}")
            return None
            
        # Processar resultado
        data = response.json()
        if not data:
            logger.error("API retornou dados vazios")
            return None
            
        # Converter para DataFrame
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        
        logger.info(f"Previsão gerada com sucesso: {len(df)} pontos")
        return df
        
    except Exception as e:
        logger.error(f"Erro ao fazer previsão: {str(e)}")
        return None


def predict_quarterly_indicator(historical_data, periods=365, indicator_name="pib"):
    """
    Função para prever valores de indicadores trimestrais como o PIB.
    """
    try:
        logger.info(f"Iniciando previsão trimestral para {indicator_name}")
        
        # Processar dados históricos
        df = pd.DataFrame(historical_data)
        
        # Verificar se temos o mínimo de dados necessários
        if df.empty:
            logger.error("Dados históricos vazios")
            return None
        
        df["data"] = pd.to_datetime(df["data"])
        
        # Converter valores para numérico, tratando strings e formatos com vírgula
        df["valor"] = df["valor"].apply(lambda x: 
            float(str(x).replace(',', '.')) if isinstance(x, (str, int, float)) else None
        )
        
        # Remover valores não numéricos
        df = df.dropna(subset=["valor"])
        
        df = df.sort_values("data")
        
        logger.info(f"Dados históricos processados: {len(df)} registros")
        
        # Verificar se ainda temos registros após conversão
        if df.empty:
            logger.error("Sem dados válidos após conversão numérica")
            return None
        
        # Obter último valor e data
        last_value = float(df["valor"].iloc[-1])
        last_date = df["data"].iloc[-1]
        
        logger.info(f"Último valor conhecido (convertido): {last_value}, data: {last_date}")
        
        # Calcular número de trimestres a prever (1 trimestre = ~90 dias)
        quarters_to_predict = max(4, periods // 90)  # Pelo menos 4 trimestres
        
        logger.info(f"Gerando previsão para {quarters_to_predict} trimestres")
        
        # Calcular taxa de crescimento média trimestral baseada nos últimos 4 trimestres
        try:
            if len(df) >= 4:
                # Obter últimos 4 pontos (presumivelmente representando trimestres)
                recent_values = df.tail(4)["valor"].values
                # Calcular crescimento médio entre trimestres consecutivos
                q_growth_rates = [(recent_values[i+1] / recent_values[i]) - 1 for i in range(len(recent_values)-1)]
                avg_growth = sum(q_growth_rates) / len(q_growth_rates)
                logger.info(f"Taxa média de crescimento trimestral calculada: {avg_growth:.4f}")
            else:
                # Taxa padrão se não temos dados suficientes
                avg_growth = 0.01  # 1% crescimento trimestral
                logger.info("Dados insuficientes, usando taxa padrão de crescimento: 0.01")
        except Exception as calc_err:
            logger.error(f"Erro ao calcular taxa de crescimento: {calc_err}")
            avg_growth = 0.01  # Taxa padrão em caso de erro
            logger.info("Usando taxa padrão de crescimento após erro: 0.01")
        
        # Criar lista para armazenar previsões
        forecast_data = []
        
        # IMPORTANTE: Adicionar o último ponto histórico como o primeiro ponto da previsão
        # Isso garante continuidade no gráfico
        forecast_data.append({
            "data": last_date,
            "valor": last_value,
            "trimestre": str(((last_date.month - 1) // 3) + 1),
            "ano": str(last_date.year),
            "confiabilidade": 1.0  # 100% de confiabilidade para dados reais
        })
        
        current_date = last_date
        current_value = last_value
        
        # Garantir que current_date é datetime e não timestamp
        if hasattr(current_date, 'to_pydatetime'):
            current_date = current_date.to_pydatetime()
        
        # Usar um fator de suavização muito mais agressivo para o primeiro trimestre
        smoothing_factor = 0.2  # Reduzido para 0.2 (crescimento MUITO mais suave)
        
        # Gerar previsões para cada trimestre
        for i in range(1, quarters_to_predict + 1):
            # Avançar para o próximo trimestre
            if current_date.month in [1, 2, 3]:
                next_date = datetime(current_date.year, 4, 15)  # Meio do 2º trimestre
                next_quarter = "2"
            elif current_date.month in [4, 5, 6]:
                next_date = datetime(current_date.year, 7, 15)  # Meio do 3º trimestre
                next_quarter = "3"
            elif current_date.month in [7, 8, 9]:
                next_date = datetime(current_date.year, 10, 15)  # Meio do 4º trimestre
                next_quarter = "4"
            else:
                next_date = datetime(current_date.year + 1, 1, 15)  # Meio do 1º trimestre (ano seguinte)
                next_quarter = "1"
            
            # Aplicar crescimento trimestral com pequena variação aleatória
            if i == 1:
                # Para o primeiro trimestre, usar taxa extremamente reduzida
                adjusted_growth = avg_growth * smoothing_factor
            elif i == 2:
                # Para o segundo trimestre, ainda usar taxa reduzida
                adjusted_growth = avg_growth * (smoothing_factor * 2)
            else:
                # Aplicar variação aleatória nos trimestres subsequentes
                random_factor = 1 + np.random.uniform(-0.15, 0.15)  # Reduzir variação para ±15%
                adjusted_growth = avg_growth * random_factor
                
            next_value = current_value * (1 + adjusted_growth)  # Aplicar crescimento
            
            # Calcular confiabilidade (diminui com cada trimestre no futuro)
            confidence = max(0.3, 0.95 - (i * 0.1))  # Começa em 95% e diminui 10% a cada trimestre
            
            logger.info(f"Previsão para {next_date}: {next_value:.2f} (trimestre {next_quarter}, confiabilidade: {confidence:.2f})")
            
            # Adicionar previsão à lista
            forecast_data.append({
                "data": next_date,
                "valor": next_value,
                "trimestre": next_quarter,
                "ano": str(next_date.year),
                "confiabilidade": confidence
            })
            
            # Atualizar valores para o próximo trimestre
            current_date = next_date
            current_value = next_value
        
        # Criar DataFrame com as previsões
        if not forecast_data:
            logger.error("Nenhum dado de previsão foi gerado")
            return None
            
        forecast_df = pd.DataFrame(forecast_data)
        logger.info(f"Previsão trimestral concluída: {len(forecast_df)} trimestres")
        return forecast_df
        
    except Exception as e:
        logger.error(f"Erro ao prever valores trimestrais para {indicator_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None