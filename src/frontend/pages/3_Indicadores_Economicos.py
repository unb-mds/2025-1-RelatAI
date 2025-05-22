import streamlit as st
import requests
import json
import datetime
import pandas as pd
import plotly.express as px
import sys
import os

# Adicionar diretório utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.data_processing import process_api_data, calculate_statistics
from utils.ml_models import predict_future_values
from utils.nlp_utils import generate_market_insights, generate_forecast_analysis

# --- Configuração da Página ---
st.set_page_config(page_title="Indicadores Econômicos - Análise", page_icon="📈", layout="wide")

st.title("Análise de Indicadores Econômicos Chave")
st.markdown("Acompanhe as tendências e previsões para SELIC, IPCA e Câmbio fornecidas pela nossa API.")

# --- Função para buscar dados da API ---
API_BASE_URL = "http://127.0.0.1:8000"

def fetch_api_data(endpoint: str, params: dict = None):
    """Busca dados de um endpoint da API e retorna o JSON, ou None em caso de erro."""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint.lstrip('/')}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dados de '{endpoint}': {e}")
        return None
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON da resposta de '{endpoint}'.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar dados de '{endpoint}': {e}")
        return None

# --- Seção para exibir os indicadores ---
tab_selic, tab_ipca, tab_cambio = st.tabs(["SELIC", "IPCA", "Câmbio"])

def display_indicator_data(indicator_name: str, api_endpoint: str, tab_container):
    with tab_container:
        st.header(f"Taxa {indicator_name}")

        # Data atual para referência
        data_atual = datetime.date.today()
        
        # --- Filtro de Data --- 
        # Modificado para permitir datas futuras
        selected_date = st.date_input(
            "Selecionar data para a análise:",
            value=data_atual,
            min_value=datetime.date(2000, 1, 1),
            # Permitir até 1 ano no futuro
            max_value=data_atual + datetime.timedelta(days=365),
            key=f"date_filter_{api_endpoint}",
            help="Selecione datas passadas para ver dados históricos ou datas futuras para previsões."
        )
        
        # Informação diferente dependendo se é data passada ou futura
        if selected_date <= data_atual:
            st.caption(f"A análise de dados históricos será carregada para: {selected_date.strftime('%d/%m/%Y')}")
        else:
            dias_futuro = (selected_date - data_atual).days
            st.caption(f"Será gerada uma previsão para: {selected_date.strftime('%d/%m/%Y')} ({dias_futuro} dias no futuro)")

        if st.button(f"Carregar Análise da {indicator_name} para {selected_date.strftime('%d/%m/%Y')}", key=f"{api_endpoint}_btn_indicadores"):
            # Para qualquer data, precisamos dos dados históricos
            with st.spinner(f"Buscando dados históricos da {indicator_name}..."):
                historical_data = fetch_api_data(api_endpoint)
            
            if not historical_data:
                st.error(f"Não foi possível obter dados históricos para {indicator_name}.")
                return
                
            # Processar dados
            df = process_api_data(historical_data)
            
            if df is None or df.empty:
                st.error(f"Dados históricos insuficientes para análise de {indicator_name}.")
                return

            # FLUXO PARA DATA PASSADA/ATUAL
            if selected_date <= data_atual:
                # Filtrar até a data selecionada
                df_filtered = df[df['data'] <= pd.Timestamp(selected_date)]
                
                if df_filtered.empty:
                    st.error(f"Não há dados disponíveis para {indicator_name} até {selected_date.strftime('%d/%m/%Y')}.")
                    return
                
                # Calcular estatísticas
                stats = calculate_statistics(df_filtered)
                
                # Mostrar gráfico histórico
                st.subheader("Dados Históricos")
                fig = px.line(df_filtered, x='data', y='valor', title=f"Histórico - {indicator_name}", 
                line_shape='spline')
                fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar estatísticas
                st.subheader("Estatísticas Principais")
                col1, col2, col3 = st.columns(3)
                col1.metric("Média", f"{stats['média']:.2f}")
                col1.metric("Mínimo", f"{stats['min']:.2f}")
                col2.metric("Mediana", f"{stats['mediana']:.2f}")
                col2.metric("Máximo", f"{stats['max']:.2f}")
                col3.metric("Desvio Padrão", f"{stats['desvio_padrão']:.2f}")
                col3.metric("Variação Percentual", f"{stats['variação_percentual']:.2f}%")
                
                # Gerar insights de mercado
                st.subheader("Análise de Mercado")
                insights = generate_market_insights(df_filtered, indicator_name)
                st.markdown(insights)
            
            # FLUXO PARA DATA FUTURA
            else:
                # Mostrar apenas o gráfico histórico para contexto
                st.subheader("Dados Históricos (Contexto)")
                fig = px.line(df, x='data', y='valor', title=f"Histórico - {indicator_name}", 
                line_shape='spline')
                st.plotly_chart(fig, use_container_width=True)
                
                
                # Pular direto para a seção de previsão
                st.subheader(f"⚡ Previsão para {selected_date.strftime('%d/%m/%Y')}")
                st.info(f"Gerando modelo preditivo para {dias_futuro} dias no futuro...")
                
                # Gerar previsão
                with st.spinner("Processando modelo de machine learning..."):
                    forecast_df = predict_future_values(
                        df,  # Pass DataFrame directly
                        periods=dias_futuro
                    )
    
                
                if forecast_df is not None:
                    # Criar DataFrame combinado para visualização
                    df_historical = df.copy().tail(30)  # últimos 30 dias
                    df_historical['tipo'] = 'histórico'
                    
                    # Obter o último ponto do histórico para criar conexão
                    last_historical_point = df_historical.iloc[-1:].copy()
                    last_historical_point['tipo'] = 'previsto'
                    
                    # Adicionar o último ponto histórico no início da previsão
                    forecast_display = forecast_df.copy()
                    forecast_display['tipo'] = 'previsto'
                    forecast_display = pd.concat([last_historical_point, forecast_display])
                    
                    # Combinar os dados
                    combined_df = pd.concat([df_historical, forecast_display])
                    
                    # Mostrar gráfico com dados históricos e previsão
                    st.subheader("Gráfico de Previsão")
                    fig = px.line(
                        combined_df, 
                        x='data', 
                        y='valor',
                        color='tipo',
                        color_discrete_map={'histórico': 'blue', 'previsto': 'red'},
                        title=f"Histórico recente e Previsão - {indicator_name}",
                        line_shape='spline'  # Suavizar linhas
                    )
                    fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))

                    # Adicionar intervalos de confiança se disponíveis
                    if 'lower_bound' in forecast_df.columns and 'upper_bound' in forecast_df.columns:
                        fig.add_scatter(
                            x=forecast_df['data'],
                            y=forecast_df['lower_bound'],
                            fill=None,
                            mode='lines',
                            line_color='rgba(255,0,0,0.1)',
                            showlegend=False
                        )


                    st.plotly_chart(fig, use_container_width=True)
                    # Mostrar confiabilidade
                    st.subheader("Confiabilidade da Previsão")
                    fig_conf = px.line(
                        forecast_df,
                        x='data',
                        y='confiabilidade',
                        title="Índice de Confiabilidade da Previsão",
                        labels={"confiabilidade": "Nível de Confiança", "data": "Data"}
                    )
                    fig_conf.update_layout(yaxis_range=[0, 1])
                    st.plotly_chart(fig_conf, use_container_width=True)
                    
                    # Gerar análise da previsão
                    st.subheader("Análise da Previsão")
                    forecast_analysis = generate_forecast_analysis(forecast_df, indicator_name)
                    st.markdown(forecast_analysis)
                    
                    # Mostrar valores específicos da previsão
                    st.subheader(f"Valores Previstos para {indicator_name}")
                    target_value = forecast_df.iloc[-1]['valor']
                    target_conf = forecast_df.iloc[-1]['confiabilidade']
                    
                    col1, col2 = st.columns(2)
                    col1.metric(f"Previsão para {selected_date.strftime('%d/%m/%Y')}", f"{target_value:.2f}")
                    col2.metric("Confiabilidade", f"{target_conf:.2%}")
                    
                    # Mostrar informações do modelo
                    st.caption("Modelo: DeepSeek (LSTM)")
                    st.caption("⚠️ A confiabilidade da previsão diminui com o horizonte temporal")
                else:
                    st.error("Não foi possível gerar previsões para a data selecionada.")

display_indicator_data("SELIC", "selic", tab_selic)
display_indicator_data("IPCA", "ipca", tab_ipca)
display_indicator_data("Câmbio", "cambio", tab_cambio)

st.sidebar.info("Navegue pelas abas para ver a análise de cada indicador.")
st.sidebar.warning("Para previsões futuras, selecione uma data após hoje.")
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")