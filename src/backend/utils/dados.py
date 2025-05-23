import pandas as pd
import requests
from io import StringIO
from datetime import timedelta

# URLs das APIs do Banco Central
URLS = {
    "selic": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv",
    "cambio": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv",
    "ipca": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv",
    "desemprego": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.24369/dados?formato=csv",
    "pib": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4380/dados?formato=csv",
    "divida": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4505/dados?formato=csv"
}

# Mapeamento dos nomes dos meses
MAPA_MESES = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
    'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
    'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
}

# Carrega e trata os dados de cada URL
def carregar_dados():
    dados = {}
    hoje = pd.Timestamp.today()

    # Períodos manuais para séries com limite de 10 anos
    limites_especiais = {
        "selic": [
    ("04/06/1986", "31/12/1995"),
    ("01/01/1996", "31/12/2005"),
    ("01/01/2006", "31/12/2015"),
    ("01/01/2016", hoje.strftime("%d/%m/%Y"))
           ],
        "cambio": [
        ("01/01/1999", "01/01/2006"), 
        ("01/01/2006", "01/01/2016"), 
        ("01/01/2016", hoje.strftime("%d/%m/%Y"))
          ]
    }

    for nome, url_base in URLS.items():
        try:
            if nome in limites_especiais:
                dfs = []
                for data_inicial, data_final in limites_especiais[nome]:
                    url = f"{url_base}&dataInicial={data_inicial}&dataFinal={data_final}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        df = pd.read_csv(StringIO(response.text), sep=';', decimal='.')
                        df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
                        df['valor'] = df['valor'].str.replace(',', '.', regex=False).astype(float)
                        df['mes'] = df['data'].dt.month_name().map(MAPA_MESES)
                        df['ano'] = df['data'].dt.year.astype(str)
                        dfs.append(df)
                dados[nome] = pd.concat(dfs).drop_duplicates(subset='data')
            else:
                response = requests.get(url_base)
                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text), sep=';', decimal='.')
                    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
                    df['valor'] = df['valor'].str.replace(',', '.', regex=False).astype(float)
                    df['mes'] = df['data'].dt.month_name().map(MAPA_MESES)
                    df['ano'] = df['data'].dt.year.astype(str)
                    dados[nome] = df
                else:
                    print(f"Erro ao acessar dados de {nome}")
        except Exception as e:
            print(f"Erro ao carregar dados de {nome}: {e}")
    return dados

# Atualiza os dados já carregados apenas para selic e cambio
def atualizar_dados(dados_existentes):
    novos_dados = {}
    atualizaveis = ['selic', 'cambio']

    for nome in dados_existentes.keys():
        if nome not in atualizaveis:
            novos_dados[nome] = dados_existentes[nome]
            continue

        try:
            df_existente = dados_existentes[nome]
            ultima_data = df_existente['data'].max()
            data_inicial = (ultima_data + timedelta(days=1)).strftime("%d/%m/%Y")
            data_final = pd.Timestamp.today().strftime("%d/%m/%Y")

            url_base = URLS[nome].split("&dataInicial=")[0]
            url = f"{url_base}&dataInicial={data_inicial}&dataFinal={data_final}"

            response = requests.get(url)
            if response.status_code == 200:
                df_novo = pd.read_csv(StringIO(response.text), sep=";", decimal=".")
                if not df_novo.empty:
                    df_novo['data'] = pd.to_datetime(df_novo['data'], format="%d/%m/%Y")
                    df_novo['valor'] = df_novo['valor'].str.replace(',', '.', regex=False).astype(float)
                    df_novo['mes'] = df_novo['data'].dt.month_name().map(MAPA_MESES)
                    df_novo['ano'] = df_novo['data'].dt.year.astype(str)
                    dados_atualizado = pd.concat([df_existente, df_novo]).drop_duplicates(subset='data')
                    novos_dados[nome] = dados_atualizado
                else:
                    novos_dados[nome] = df_existente
            else:
                novos_dados[nome] = df_existente
        except Exception as e:
            print(f"Erro ao atualizar dados de {nome}: {e}")
            novos_dados[nome] = dados_existentes[nome]

    return novos_dados

# Filtrar DataFrame por ano e mês
def filtrar_por_ano_mes(df, ano: str, mes: str):
    return df[(df['ano'] == ano) & (df['mes'].str.lower() == mes.lower())]

# Cálculo de média mensal
def media_mensal(df, ano, mes):
    ano = str(ano)
    mes = mes.lower()
    df_mes = df[(df['ano'] == ano) & (df['mes'].str.lower() == mes)]
    if df_mes.empty:
        return f"Nenhum dado encontrado para {mes}/{ano}."
    return round(df_mes['valor'].mean(), 2)

# Cálculo de média anual
def media_anual(df, ano):
    ano = str(ano)
    df_ano = df[df['ano'] == ano]
    if df_ano.empty:
        return f"Nenhum dado encontrado para o ano {ano}."
    return round(df_ano['valor'].mean(), 2)



#1. Carregar os dados iniciais
#dados = carregar_dados()

#2. Atualizar os dados até a data atual
#dados_atualizados = atualizar_dados(dados["selic"], dados["cambio"], dados["ipca"])

#Agora você pode acessar os DataFrames atualizados:
#df_selic = dados_atualizados["selic"]
#df_cambio = dados_atualizados["cambio"]
#df_ipca = dados_atualizados["ipca"]

#Para ver
#df_ipca
#df_cambio
#df_selic

#3. Exemplo: filtrar dados de câmbio para Março de 2024
#df_filtrado = filtrar_por_ano_mes(df_cambio, "2024", "março")

#4. Ver os dados
#print(df_filtrado)

#5. Filtrar por media
#print(media_anual(dados["ipca"], 2022))          # Ex: 5.10
#print(media_mensal(dados["ipca"], 2022, "Março"))  # Ex: 1.32