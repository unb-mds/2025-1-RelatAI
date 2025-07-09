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
from utils.ml_client import predict_future_values
from utils.nlp_utils import generate_market_insights, generate_forecast_analysis

# --- Configuração da Página ---
st.set_page_config(page_title="Indicadores Econômicos - Análise", page_icon="📈", layout="wide")

st.title("Análise de Indicadores Econômicos Chave")
st.markdown("Acompanhe as tendências e previsões para SELIC, IPCA e Câmbio fornecidas pela nossa API.")

# --- Função para buscar dados da API ---
API_BASE_URL = "http://backend:8000"

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

def format_indicator_value(value, indicator_name):
    """
    Formata o valor do indicador de acordo com seu tipo
    """
    indicator = indicator_name.upper()
    
    if indicator == "SELIC":
        # SELIC é fornecida como decimal (ex: 0.03 para 3%), então multiplicar por 100
        return f"{value * 100:.2f}%"
    elif indicator == "IPCA":
        # IPCA também pode precisar de ajuste dependendo de como os dados são fornecidos
        return f"{value:.2f}%"
    elif indicator == "CÂMBIO":
        # Câmbio é em reais
        return f"R$ {value:.2f}"
    elif indicator == "PIB":
        # PIB geralmente é em bilhões ou trilhões
        if value >= 1000:
            return f"R$ {value/100000:.2f} tri"
        else:
            return f"R$ {value:.2f} bi"
        
    elif indicator == "DÍVIDA PÚBLICA" or indicator == "DIVIDA" or indicator == "DÍVIDA":
        # Dívida pública em bilhões ou trilhões, similar ao PIB
        if value >= 1000:
            return f"R$ {value/1000:.2f} tri"
        else:
            return f"R$ {value:.2f} bi"
        
    elif indicator == "DESEMPREGO":
        # Desemprego é em percentual
        return f"{value:.2f}%"
    
    else:
        # Formato padrão para outros indicadores
        return f"{value:.2f}"

# --- Seção para exibir os indicadores ---
tab_selic, tab_ipca, tab_cambio, tab_pib, tab_divida, tab_desemprego = st.tabs(["SELIC", "IPCA", "Câmbio", "PIB", "Dívida Pública", "Desemprego"])

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
                stats = calculate_statistics(df_filtered)  # Usar os dados filtrados até a data selecionada
                
                # Mostrar gráfico histórico
                st.subheader("Dados Históricos")
                fig = px.line(df_filtered, x='data', y='valor', title=f"Histórico - {indicator_name}", 
                line_shape='spline')
                fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar estatísticas
                st.subheader("Estatísticas Principais")
                col1, col2, col3 = st.columns(3)
                col1.metric("Média", format_indicator_value(stats['média'], indicator_name))
                col1.metric("Mínimo", format_indicator_value(stats['min'], indicator_name))
                col2.metric("Mediana", format_indicator_value(stats['mediana'], indicator_name))
                col2.metric("Máximo", format_indicator_value(stats['max'], indicator_name))
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
                    historical_data, 
                    periods=dias_futuro, 
                    model_type="deepseek"
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
                    col1.metric(f"Previsão para {selected_date.strftime('%d/%m/%Y')}", format_indicator_value(target_value, indicator_name))
                    col2.metric("Confiabilidade", f"{target_conf:.2%}")
                    
                    # Mostrar informações do modelo
                    st.caption("Modelo: DeepSeek (LSTM)")
                    st.caption("⚠️ A confiabilidade da previsão diminui com o horizonte temporal")
                else:
                    st.error("Não foi possível gerar previsões para a data selecionada.")

display_indicator_data("SELIC", "selic", tab_selic)
display_indicator_data("IPCA", "ipca", tab_ipca)
display_indicator_data("Câmbio", "cambio", tab_cambio)
display_indicator_data("Dívida Pública", "divida", tab_divida)
display_indicator_data("Desemprego", "desemprego", tab_desemprego)

# --- Função para exibir indicadores trimestrais (ex: PIB) ---
def display_quarterly_indicator(indicator_name: str, api_endpoint: str, tab_container):
    """
    Função para exibir indicadores com periodicidade trimestral (PIB, dívida pública, etc.)
    """
    with tab_container:
        st.header(f"{indicator_name}")

        # Data atual para referência
        data_atual = datetime.date.today()
        
        # --- Filtro por Ano e Trimestre --- 
        col1, col2 = st.columns(2)
        
        with col1:
            # Anos de 2010 até ano atual + 1
            selected_year = st.selectbox(
                "Ano:",
                options=list(range(2010, data_atual.year + 2)),
                index=data_atual.year - 2010,  # Seleciona o ano atual por padrão
                key=f"{api_endpoint}_year_filter"
            )
        
        with col2:
            selected_trimestre = st.selectbox(
                "Trimestre:",
                options=["1", "2", "3", "4"],
                index=min((data_atual.month - 1) // 3, 3),  # Trimestre atual por padrão
                key=f"{api_endpoint}_trimestre_filter"
            )
        
        # Determinar se a data selecionada é futura
        trimestre_atual = (data_atual.month - 1) // 3 + 1
        is_future = (selected_year > data_atual.year) or (selected_year == data_atual.year and int(selected_trimestre) > trimestre_atual)
        
        # Informação diferente dependendo se é histórico ou previsão
        if not is_future:
            st.caption(f"A análise de dados históricos será carregada para: {selected_trimestre}º Trimestre/{selected_year}")
        else:
            st.caption(f"Será gerada uma previsão para: {selected_trimestre}º Trimestre/{selected_year}")

        # Botão para carregar dados ou previsão
        button_text = f"Carregar Análise do {indicator_name} para {selected_trimestre}º Trimestre/{selected_year}"
        
        if st.button(button_text, key=f"{api_endpoint}_btn_indicadores"):
            # Para qualquer opção, precisamos dos dados históricos
            with st.spinner(f"Buscando dados históricos do {indicator_name}..."):
                historical_data = fetch_api_data(api_endpoint)
            
            if not historical_data:
                st.error(f"Não foi possível obter dados históricos para {indicator_name}.")
                return
                
            # Processar dados
            df = process_api_data(historical_data)
            
            if df is None or df.empty:
                st.error(f"Dados históricos insuficientes para análise do {indicator_name}.")
                return
                
            # Adicionar trimestre para dados processados
            df['trimestre'] = ((pd.to_datetime(df['data']).dt.month - 1) // 3 + 1).astype(str)
            df['ano'] = pd.to_datetime(df['data']).dt.year.astype(str)

            # FLUXO PARA DADOS HISTÓRICOS
            if not is_future:
                # Filtrar por ano e trimestre
                df_filtered = df[(df['ano'] == str(selected_year)) & (df['trimestre'] == selected_trimestre)]
                
                if df_filtered.empty:
                    st.error(f"Não há dados disponíveis para o {indicator_name} no {selected_trimestre}º trimestre de {selected_year}.")
                    return
                
                # Filtrar dados do ano para estatísticas
                df_year = df[df['ano'] == str(selected_year)]
                
                # Calcular estatísticas com dados de todo o ano
                stats = calculate_statistics(df_year)  # Usar todos os dados do ano, não apenas um trimestre
    
                # Mostrar gráfico histórico 
                st.subheader("Dados Históricos")
                
                # Preparar dados para visualização trimestral
                df_plot = df.copy()
                df_plot['data'] = pd.to_datetime(df_plot['data'])
                df_plot = df_plot.sort_values('data')
                
                fig = px.line(df_plot, x='data', y='valor', title=f"Histórico do {indicator_name}", 
                             line_shape='spline')
                fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                
                # Destaque para o trimestre selecionado
                fig.add_scatter(
                    x=df_filtered['data'], 
                    y=df_filtered['valor'],
                    mode='markers',
                    marker=dict(size=12, color='red'),
                    name=f"{selected_trimestre}º Trimestre/{selected_year}"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar estatísticas
                st.subheader("Estatísticas Principais")
                col1, col2, col3 = st.columns(3)
                col1.metric("Média", format_indicator_value(stats['média'], indicator_name))
                col1.metric("Mínimo", format_indicator_value(stats['min'], indicator_name))
                col2.metric("Mediana", format_indicator_value(stats['mediana'], indicator_name))
                col2.metric("Máximo", format_indicator_value(stats['max'], indicator_name))
                col3.metric("Desvio Padrão", f"{stats['desvio_padrão']:.2f}")
                col3.metric("Variação Percentual", f"{stats['variação_percentual']:.2f}%")
                
                # Dados do ano selecionado
                st.subheader(f"Dados Trimestrais de {selected_year}")
                df_year = df[df['ano'] == str(selected_year)]
                
                if not df_year.empty:
                    # Organizar dados trimestrais em tabela
                    quarters_data = []
                    for q in ["1", "2", "3", "4"]:
                        q_data = df_year[df_year['trimestre'] == q]
                        if not q_data.empty:
                            quarters_data.append({
                            "Trimestre": f"{q}º/{selected_year}",
                            "Valor": format_indicator_value(q_data['valor'].values[0], indicator_name),
                            "Data": pd.to_datetime(q_data['data'].values[0]).strftime('%d/%m/%Y')
                        })
                    
                    if quarters_data:
                        st.table(pd.DataFrame(quarters_data))
                
                # Gerar insights de mercado
                st.subheader("Análise de Mercado")
                insights = generate_market_insights(df_filtered, indicator_name)
                st.markdown(insights)
            
            # FLUXO PARA PREVISÃO
            else:
                # Mostrar gráfico histórico para contexto
                st.subheader("Dados Históricos (Contexto)")
                
                # Preparar dados para visualização
                df_plot = df.copy()
                df_plot['data'] = pd.to_datetime(df_plot['data'])
                df_plot = df_plot.sort_values('data')
                
                fig = px.line(df_plot, x='data', y='valor', title=f"Histórico do {indicator_name}", 
                             line_shape='spline')
                st.plotly_chart(fig, use_container_width=True)
                
                # Calcular dias no futuro para a previsão
                # Estimativa da data do meio do trimestre escolhido
                trimestre_meses = {
                    "1": 2,  # Fevereiro (meio do 1º trim)
                    "2": 5,  # Maio (meio do 2º trim)
                    "3": 8,  # Agosto (meio do 3º trim)
                    "4": 11  # Novembro (meio do 4º trim)
                }
                
                data_alvo = datetime.date(selected_year, trimestre_meses[selected_trimestre], 15)
                dias_futuro = (data_alvo - data_atual).days
                dias_futuro = max(dias_futuro, 30)  # Pelo menos 30 dias
                
                # Seção de previsão
                st.subheader(f"⚡ Previsão para o {selected_trimestre}º Trimestre de {selected_year}")
                st.info(f"Gerando modelo preditivo para aproximadamente {dias_futuro} dias no futuro...")
                
                # Gerar previsão
                with st.spinner("Processando modelo de machine learning..."):
                    forecast_df = predict_future_values(
                        historical_data, 
                        periods=dias_futuro, 
                        model_type="deepseek",
                        indicator_name=api_endpoint  # Passa o nome do indicador
                    )
                
                if forecast_df is not None:
                    # Processar dados da previsão
                    forecast_df['data'] = pd.to_datetime(forecast_df['data'])
                    forecast_df['trimestre'] = ((forecast_df['data'].dt.month - 1) // 3 + 1).astype(str)
                    forecast_df['ano'] = forecast_df['data'].dt.year.astype(str)
                    
                    # Filtrar a previsão para o trimestre específico
                    forecast_trimestre = forecast_df[
                        (forecast_df['ano'] == str(selected_year)) & 
                        (forecast_df['trimestre'] == selected_trimestre)
                    ]
                    
                    # Substituir o trecho atual (aproximadamente linhas 436-465) por este:
                    if not forecast_trimestre.empty:
                        # Usar o valor médio previsto para o trimestre
                        trimestre_valor = forecast_trimestre['valor'].mean()
                        trimestre_conf = forecast_trimestre['confiabilidade'].mean() if 'confiabilidade' in forecast_trimestre.columns else 0.85
                        
                        # Preparar dados para o gráfico
                        df_historical = df_plot.tail(12).copy()  
                        df_historical['tipo'] = 'histórico'
                        
                        # Obter o último ponto do histórico para criar conexão
                        last_date = df_historical['data'].max()
                        last_value = df_historical[df_historical['data'] == last_date]['valor'].values[0]
                        
                        # Preparar dados de previsão
                        forecast_display = forecast_df.copy()
                        forecast_display = forecast_display[forecast_display['data'] > last_date]
                        forecast_display['tipo'] = 'previsto'

                        transition_point = pd.DataFrame([{
                            'data': last_date + pd.Timedelta(days=1),  # Um dia após o último histórico
                            'valor': last_value,  # MESMO valor do último histórico
                            'tipo': 'previsto',
                            'trimestre': df_historical.iloc[-1]['trimestre'],
                            'ano': df_historical.iloc[-1]['ano'],
                            'confiabilidade': 1.0
                        }])
                        
                        # Adicionar o último ponto histórico no início da previsão para criar transição
                        forecast_display = pd.concat([transition_point, forecast_display])
                        combined_df = pd.concat([df_historical, forecast_display])
                        combined_df = combined_df.sort_values('data')
        
                        
                        # Mostrar gráfico com dados históricos e previsão
                        st.subheader("Gráfico de Previsão")

                        fig = px.line(
                            combined_df, 
                            x='data', 
                            y='valor',
                            color='tipo',
                            color_discrete_map={'histórico': 'blue', 'previsto': 'red'},
                            title=f"Histórico recente e Previsão - {indicator_name}",
                            line_shape='spline'
                        )

                        # Reduzir muito a suavização para evitar que as curvas ultrapassem pontos críticos
                        fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                        
                        # Destacar o trimestre específico da previsão
                        target_quarter = forecast_display[
                            (forecast_display['data'].dt.year == selected_year) & 
                            ((forecast_display['data'].dt.month - 1) // 3 + 1 == int(selected_trimestre))
                        ]

                        if not target_quarter.empty:
                            fig.add_scatter(
                                x=target_quarter['data'],
                                y=target_quarter['valor'],
                                mode='markers',
                                marker=dict(size=10, color='darkred', symbol='circle'),  # Mudado de 'star' para 'circle'
                                name=f"Previsão para {selected_trimestre}º Trim/{selected_year}"
                            )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Mostrar valores específicos da previsão
                        st.subheader(f"Valor Previsto para {indicator_name}")
                        
                        col1, col2 = st.columns(2)
                        col1.metric(f"{selected_trimestre}º Trimestre/{selected_year}", format_indicator_value(trimestre_valor, indicator_name))
                        col2.metric("Confiabilidade", f"{trimestre_conf:.2%}")
                        
                        # Confiabilidade da previsão
                        st.subheader("Confiabilidade da Previsão")

                        # Verificar se a coluna confiabilidade existe antes de tentar usá-la
                        if 'confiabilidade' in forecast_df.columns:
                            fig_conf = px.line(
                                forecast_df,
                                x='data',
                                y='confiabilidade',
                                title="Índice de Confiabilidade da Previsão",
                                labels={"confiabilidade": "Nível de Confiança", "data": "Data"}
                            )
                        else:
                            # Se não existir, criar um DataFrame básico com confiabilidade padrão
                            conf_df = forecast_df.copy()
                            conf_df['confiabilidade'] = [max(0.3, 0.95 - (i * 0.1)) for i in range(len(conf_df))]
                            fig_conf = px.line(
                                conf_df,
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
                        
                        # Mostrar informações do modelo
                        st.caption("Modelo: DeepSeek (LSTM)")
                        st.caption("⚠️ A confiabilidade da previsão diminui com o horizonte temporal")
                    else:
                        st.error(f"Não foi possível gerar previsões específicas para o {selected_trimestre}º trimestre de {selected_year}.")
                else:
                    st.error("Não foi possível gerar previsões para a data selecionada.")
                    
# Exibir a aba do PIB com a nova função
display_quarterly_indicator("PIB", "pib", tab_pib)

st.sidebar.info("Navegue pelas abas para ver a análise de cada indicador.")
st.sidebar.warning("Para previsões futuras, selecione uma data após hoje.")
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")