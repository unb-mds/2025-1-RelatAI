import pandas as pd
import requests
from io import StringIO

# URL da API do Banco Central para consulta de dados financeiros
URL_BC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv"

# Carrega os dados de um arquivo CSV local (modo offline ou backup)
def carregar_dados():
    return pd.read_csv("data/dados_ipea.csv")

# Faz requisição à API do BC, trata e retorna o DataFrame atualizado
def baixar_dados_banco_central():
    response = requests.get(URL_BC)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text), sep=";")
        df.columns = [c.strip().lower() for c in df.columns]  # Normaliza colunas
        df.rename(columns={"data": "data", "valor": "valor"}, inplace=True)
        df["data"] = pd.to_datetime(df["data"], dayfirst=True)  # Converte datas
        df["ano"] = df["data"].dt.year  # Extrai ano
        return df
    else:
        raise Exception("Erro ao acessar API do Banco Central")
