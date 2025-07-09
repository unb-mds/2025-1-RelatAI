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

MAPA_MESES = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
    'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
    'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
}

import pandas as pd

def converter_data_safe(df, coluna="data"):
    try:
        # Deixe o pandas inferir automaticamente o formato
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce', utc=False)
        return df
    except Exception as e:
        print(f"Erro ao converter datas: {e}")
        return df


def carregar_dados():
    dados = {}
    hoje = pd.Timestamp.today()

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

                        # Conversão robusta de datas
                        df = converter_data_safe(df, coluna='data')

                        
                        # Remove linhas com datas inválidas
                        df = df.dropna(subset=['data'])
                        
                        if df['valor'].dtype == object:
                            df['valor'] = df['valor'].str.replace(',', '.', regex=False).astype(float)
                        df['mes'] = df['data'].dt.month_name().map(MAPA_MESES)
                        df['ano'] = df['data'].dt.year.astype(str)
                        if nome == "pib":
                            df['trimestre'] = df['data'].dt.month.apply(lambda m: str((m - 1) // 3 + 1))
                        dfs.append(df)
                dados[nome] = pd.concat(dfs).drop_duplicates(subset='data')
            else:
                response = requests.get(url_base)
                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text), sep=';', decimal='.')
                    
                    # Conversão robusta de datas
                    df = converter_data_safe(df, coluna='data')

                    
                    # Remove linhas com datas inválidas
                    df = df.dropna(subset=['data'])
                    
                    if df['valor'].dtype == object:
                        df['valor'] = df['valor'].str.replace(',', '.', regex=False).astype(float)
                    df['mes'] = df['data'].dt.month_name().map(MAPA_MESES)
                    df['ano'] = df['data'].dt.year.astype(str)
                    if nome == "pib":
                        df['trimestre'] = df['data'].dt.month.apply(lambda m: str((m - 1) // 3 + 1))
                    dados[nome] = df
                else:
                    print(f"Erro ao acessar dados de {nome}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Erro ao carregar dados de {nome}: {e}")
    return dados


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

            data_inicial_dt = ultima_data
            data_final_dt = pd.Timestamp.today() - timedelta(days=1)

            # Impede chamada inválida à API
            if data_inicial_dt >= data_final_dt:
                novos_dados[nome] = df_existente
                continue

            data_inicial = data_inicial_dt.strftime("%d/%m/%Y")
            data_final = data_final_dt.strftime("%d/%m/%Y")
            url = f"{URLS[nome]}&dataInicial={data_inicial}&dataFinal={data_final}"

            response = requests.get(url)
            if response.status_code == 200:
                df_novo = pd.read_csv(StringIO(response.text), sep=";", decimal=".")
                if not df_novo.empty:
                    # Conversão robusta de datas
                    df = converter_data_safe(df, coluna='data')

                    
                    # Remove linhas com datas inválidas
                    df_novo = df_novo.dropna(subset=['data'])
                    
                    if df_novo['valor'].dtype == object:
                        df_novo['valor'] = df_novo['valor'].str.replace(',', '.', regex=False).astype(float)
                    df_novo['mes'] = df_novo['data'].dt.month_name().map(MAPA_MESES)
                    df_novo['ano'] = df_novo['data'].dt.year.astype(str)
                    if nome == "pib":
                        df_novo['trimestre'] = df_novo['data'].dt.month.apply(lambda m: str((m - 1) // 3 + 1))
                    dados_atualizado = pd.concat([df_existente, df_novo]).drop_duplicates(subset='data')
                    novos_dados[nome] = dados_atualizado
                else:
                    novos_dados[nome] = df_existente
            else:
                print(f"Erro ao atualizar {nome}: HTTP {response.status_code}")
                novos_dados[nome] = df_existente
        except Exception as e:
            print(f"Erro ao atualizar dados de {nome}: {e}")
            novos_dados[nome] = dados_existentes[nome]

    return novos_dados


def filtrar_por_ano_mes(df, ano: str, mes: str):
    return df[(df['ano'] == ano) & (df['mes'].str.lower() == mes.lower())]

def media_mensal(df, ano, mes):
    ano = str(ano)
    mes = mes.lower()
    df_mes = df[(df['ano'] == ano) & (df['mes'].str.lower() == mes)]
    if df_mes.empty:
        return f"Nenhum dado encontrado para {mes}/{ano}."
    return round(df_mes['valor'].mean(), 2)

def media_anual(df, ano):
    ano = str(ano)
    df_ano = df[df['ano'] == ano]
    if df_ano.empty:
        return f"Nenhum dado encontrado para o ano {ano}."
    return round(df_ano['valor'].mean(), 2)

def filtrar_pib_por_ano_trimestre(df_pib, ano: str, trimestre: str = None):
    if trimestre is None:
        return df_pib[df_pib['ano'] == ano]
    else:
        return df_pib[(df_pib['ano'] == ano) & (df_pib['trimestre'] == trimestre)]
