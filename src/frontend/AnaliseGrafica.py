import streamlit as st
import requests

st.title("Análise Econômica - Filtro por Ano e Mês")

# Seleção de qual DataFrame o usuário quer ver
opcao = st.selectbox("Escolha o conjunto de dados:", ["IPCA", "Câmbio", "SELIC"])

# Fazendo a requisição para pegar todos os dados (sem filtro inicial)
if opcao == "IPCA":
    url = "http://localhost:8000/api/ipca/all"
elif opcao == "Câmbio":
    url = "http://localhost:8000/api/cambio/all"
else:
    url = "http://localhost:8000/api/selic/all"

# Requisição para a API para pegar os dados completos
response = requests.get(url)

if response.status_code == 200:
    df = response.json()  # Recebe os dados brutos da API

    # Pegando os anos e meses dinamicamente do DataFrame
    anos_disponiveis = sorted(set([item['ano'] for item in df]))  # Extrai os anos
    meses_disponiveis = sorted(set([item['mes'] for item in df]))  # Extrai os meses

    # Interface para escolha de ano e mês
    ano_escolhido = st.selectbox("Selecione o ano:", anos_disponiveis)
    mes_escolhido = st.selectbox("Selecione o mês:", meses_disponiveis)

    # Realiza a requisição para a API com o filtro de ano e mês
    if opcao == "IPCA":
        url_filtro = f"http://localhost:8000/api/ipca?ano={ano_escolhido}&mes={mes_escolhido}"
    elif opcao == "Câmbio":
        url_filtro = f"http://localhost:8000/api/cambio?ano={ano_escolhido}&mes={mes_escolhido}"
    else:
        url_filtro = f"http://localhost:8000/api/selic?ano={ano_escolhido}&mes={mes_escolhido}"

    # Fazendo a requisição para a API com o filtro aplicado
    response_filtrado = requests.get(url_filtro)

    if response_filtrado.status_code == 200:
        df_filtrado = response_filtrado.json()  # Recebe os dados filtrados
        st.subheader(f"{opcao} - {mes_escolhido}/{ano_escolhido}")
        st.dataframe(df_filtrado)
    else:
        st.error(f"Erro ao carregar dados filtrados: {response_filtrado.status_code}")
else:
    st.error(f"Erro ao carregar dados: {response.status_code}")
