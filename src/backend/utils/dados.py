import pandas as pd
import requests
from io import StringIO

# URLs das APIs do Banco Central
URL_SELIC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_CAMBIO = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_IPCA = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv"  # IPCA é mensal, não precisa limitar


# Baixar dados diretamente (sem tratamento)
response_selic = requests.get(URL_SELIC)
response_cambio = requests.get(URL_CAMBIO)
response_ipca = requests.get(URL_IPCA)

# Converter respostas em DataFrame bruto
df_selic = pd.read_csv(StringIO(response_selic.text), sep=";", decimal=",") #Transform de tipo texto em String, declara que ; é separação, e declara que ontem tem número com , signific que é decimal e transforma para .
df_cambio = pd.read_csv(StringIO(response_cambio.text), sep=";", decimal=",")
df_ipca = pd.read_csv(StringIO(response_ipca.text), sep=";", decimal=",")
pd.set_option('display.max_columns', None) #mostrar o maximo de colunas existentes

# transformar coluna data para tipo datetime em pandas
df_ipca['data'] = pd.to_datetime(df_ipca['data'], format="%d/%m/%Y")
df_cambio['data'] = pd.to_datetime(df_cambio['data'], format="%d/%m/%Y")
df_selic['data'] = pd.to_datetime(df_selic['data'], format="%d/%m/%Y")

# criando coluna mês 
df_cambio['mes'] = df_cambio['data'].dt.month_name()
df_ipca['mes'] = df_ipca['data'].dt.month_name()
df_selic['mes'] = df_selic['data'].dt.month_name()

# criando coluna ano
df_cambio['ano'] = df_cambio['data'].dt.year.astype(str)
df_ipca['ano'] = df_ipca['data'].dt.year.astype(str)
df_selic['ano'] = df_selic['data'].dt.year.astype(str)


def filtrar_por_ano_mes(df, ano: str, mes: str):
    
    return df[
        (df['ano'] == ano) & 
        (df['mes'].str.lower() == mes.lower())
    ]
