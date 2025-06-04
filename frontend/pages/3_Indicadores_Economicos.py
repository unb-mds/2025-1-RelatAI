import streamlit as st
import requests
import json
import datetime # Adicionar import para datetime

# --- Configuração da Página ---
st.set_page_config(page_title="Indicadores Econômicos - Análise", page_icon="📈", layout="wide")

st.title("Análise de Indicadores Econômicos Chave")
st.markdown("Acompanhe as tendências e previsões para SELIC, IPCA e Câmbio fornecidas pela nossa API.")

# --- Função para buscar dados da API (Reutilizada e Modificada) ---
API_BASE_URL = "http://127.0.0.1:8000"

def fetch_api_data(endpoint: str, params: dict = None): # Adicionado params
    """Busca dados de um endpoint da API e retorna o JSON, ou None em caso de erro."""
    try:
        # Adicionado o argumento 'params' à chamada requests.get
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

        # --- Filtro de Data ---
        # Usar uma chave única para cada date_input para evitar conflitos entre abas
        selected_date = st.date_input(
            "Selecionar data para a análise:",
            value=datetime.date.today(), # Data padrão é hoje
            min_value=datetime.date(2000, 1, 1), # Exemplo de data mínima
            max_value=datetime.date.today(),     # Exemplo de data máxima
            key=f"date_filter_{api_endpoint}"
        )
        
        # Informar ao usuário que a data será usada na próxima carga
        st.caption(f"A análise será carregada para a data selecionada: {selected_date.strftime('%d/%m/%Y')}")

        if st.button(f"Carregar Análise da {indicator_name} para {selected_date.strftime('%d/%m/%Y')}", key=f"{api_endpoint}_btn_indicadores"):
            # Formatar a data para enviar como parâmetro para a API (ex: YYYY-MM-DD)
            date_param_str = selected_date.strftime("%Y-%m-%d")
            api_params = {"data": date_param_str} # Assumindo que a API espera um parâmetro 'data'

            with st.spinner(f"Buscando dados da {indicator_name} para {selected_date.strftime('%d/%m/%Y')}..."):
                data = fetch_api_data(api_endpoint, params=api_params)
            
            if data and isinstance(data, dict):
                st.markdown(f"#### Análise de Tendência para {selected_date.strftime('%d/%m/%Y')}")
                st.info(data.get('descricao', 'Descrição não disponível.'))
                st.divider()
                
                col1, col2 = st.columns(2)
                col1.metric("Tendência Geral", data.get("tendencia", "N/A").capitalize())
                # A previsão de 30 dias seria a partir da 'selected_date' se a API calcular assim
                col2.metric(f"Previsão (30 dias após {selected_date.strftime('%d/%m/%Y')})", f"{data.get('previsao_30_dias', 0.0):.2f}")
                
                col3, col4 = st.columns(2)
                # Estes valores seriam relativos à 'selected_date' se a API os calcular assim
                col3.metric("Maior Valor (contexto da data)", f"{data.get('maior_valor', 0.0):.2f}")
                col4.metric("Menor Valor (contexto da data)", f"{data.get('menor_valor', 0.0):.2f}")

                # Se a API retornar a série histórica completa para a data ou período, poderíamos adicionar um gráfico aqui.
                # Exemplo: if 'serie_historica' in data and data['serie_historica']:
                # import pandas as pd # Mover import para o topo do arquivo se usar pandas
                # try:
                #     df = pd.DataFrame(data['serie_historica'])
                #     if 'data' in df.columns and 'valor' in df.columns:
                #         df['data'] = pd.to_datetime(df['data'])
                #         st.line_chart(df.set_index('data')['valor'])
                #     else:
                #         st.warning("Dados da série histórica incompletos para gerar gráfico.")
                # except Exception as e:
                #     st.error(f"Erro ao processar série histórica para gráfico: {e}")

            elif data: 
                st.warning(f"Formato de dados inesperado para {indicator_name}.")
                st.json(data) 
            else:
                st.warning(f"Não foi possível carregar os dados da {indicator_name} para {selected_date.strftime('%d/%m/%Y')} no momento.")

display_indicator_data("SELIC", "selic", tab_selic)
display_indicator_data("IPCA", "ipca", tab_ipca)
display_indicator_data("Câmbio", "cambio", tab_cambio)

st.sidebar.info("Navegue pelas abas para ver a análise de cada indicador.")
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")