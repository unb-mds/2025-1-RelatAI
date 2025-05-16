import pandas as pd
import requests
from io import StringIO

# URLs das APIs do Banco Central
URL_SELIC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_CAMBIO = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_IPCA = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv"

# Função para carregar os dados diretamente da API
def carregar_dados():
    try:
        # Baixar dados diretamente (sem tratamento)
        response_selic = requests.get(URL_SELIC)
        response_cambio = requests.get(URL_CAMBIO)
        response_ipca = requests.get(URL_IPCA)

        # Verifica se as requisições foram bem-sucedidas
        if response_selic.status_code == 200 and response_cambio.status_code == 200 and response_ipca.status_code == 200:
            # Converter respostas em DataFrame bruto
            df_selic = pd.read_csv(StringIO(response_selic.text), sep=";", decimal=",")
            df_cambio = pd.read_csv(StringIO(response_cambio.text), sep=";", decimal=",")
            df_ipca = pd.read_csv(StringIO(response_ipca.text), sep=";", decimal=",")
            
            # transformar coluna data para tipo datetime em pandas
            df_ipca['data'] = pd.to_datetime(df_ipca['data'], format="%d/%m/%Y")
            df_cambio['data'] = pd.to_datetime(df_cambio['data'], format="%d/%m/%Y")
            df_selic['data'] = pd.to_datetime(df_selic['data'], format="%d/%m/%Y")

            # criando coluna mês e ano
            df_cambio['mes'] = df_cambio['data'].dt.month_name()
            df_ipca['mes'] = df_ipca['data'].dt.month_name()
            df_selic['mes'] = df_selic['data'].dt.month_name()

            df_cambio['ano'] = df_cambio['data'].dt.year.astype(str)
            df_ipca['ano'] = df_ipca['data'].dt.year.astype(str)
            df_selic['ano'] = df_selic['data'].dt.year.astype(str)

            return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca}
        else:
            raise Exception("Erro ao acessar as APIs do Banco Central.")
    except Exception as e:
        print(f"Erro ao carregar dados da API: {e}")
        return None

from datetime import timedelta

# Função para atualizar os DataFrames existentes com novos dados da API
def atualizar_dados(df_selic, df_cambio, df_ipca):
    try:
        # Obtém a última data de cada DataFrame
        ultima_data_selic = df_selic['data'].max()
        ultima_data_cambio = df_cambio['data'].max()
        ultima_data_ipca = df_ipca['data'].max()

        # Define a data inicial para a próxima consulta (um dia após o último dado)
        data_inicial_selic = (ultima_data_selic + timedelta(days=1)).strftime("%d/%m/%Y")
        data_inicial_cambio = (ultima_data_cambio + timedelta(days=1)).strftime("%d/%m/%Y")
        data_inicial_ipca = (ultima_data_ipca + timedelta(days=1)).strftime("%d/%m/%Y")

        data_final = pd.Timestamp.today().strftime("%d/%m/%Y")

        # URLs com intervalo atualizado
        url_selic = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv&dataInicial={data_inicial_selic}&dataFinal={data_final}"
        url_cambio = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial={data_inicial_cambio}&dataFinal={data_final}"
        url_ipca = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv&dataInicial={data_inicial_ipca}&dataFinal={data_final}"

        # Requisições
        response_selic = requests.get(url_selic)
        response_cambio = requests.get(url_cambio)
        response_ipca = requests.get(url_ipca)

        # Verificação
        if response_selic.status_code == 200:
            novos_dados_selic = pd.read_csv(StringIO(response_selic.text), sep=";", decimal=",")
            if not novos_dados_selic.empty:
                novos_dados_selic['data'] = pd.to_datetime(novos_dados_selic['data'], format="%d/%m/%Y")
                novos_dados_selic['mes'] = novos_dados_selic['data'].dt.month_name()
                novos_dados_selic['ano'] = novos_dados_selic['data'].dt.year.astype(str)
                df_selic = pd.concat([df_selic, novos_dados_selic]).drop_duplicates(subset='data')

        if response_cambio.status_code == 200:
            novos_dados_cambio = pd.read_csv(StringIO(response_cambio.text), sep=";", decimal=",")
            if not novos_dados_cambio.empty:
                novos_dados_cambio['data'] = pd.to_datetime(novos_dados_cambio['data'], format="%d/%m/%Y")
                novos_dados_cambio['mes'] = novos_dados_cambio['data'].dt.month_name()
                novos_dados_cambio['ano'] = novos_dados_cambio['data'].dt.year.astype(str)
                df_cambio = pd.concat([df_cambio, novos_dados_cambio]).drop_duplicates(subset='data')

        if response_ipca.status_code == 200:
            novos_dados_ipca = pd.read_csv(StringIO(response_ipca.text), sep=";", decimal=",")
            if not novos_dados_ipca.empty:
                novos_dados_ipca['data'] = pd.to_datetime(novos_dados_ipca['data'], format="%d/%m/%Y")
                novos_dados_ipca['mes'] = novos_dados_ipca['data'].dt.month_name()
                novos_dados_ipca['ano'] = novos_dados_ipca['data'].dt.year.astype(str)
                df_ipca = pd.concat([df_ipca, novos_dados_ipca]).drop_duplicates(subset='data')

        return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca}

    except Exception as e:
        print(f"Erro ao atualizar os dados: {e}")
        return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca}


# Função de filtro por ano e mês
def filtrar_por_ano_mes(df, ano: str, mes: str):
    return df[(df['ano'] == ano) & (df['mes'].str.lower() == mes.lower())]



## 1. Carregar os dados iniciais
# = carregar_dados()

# 2. Atualizar os dados até a data atual
#dados_atualizados = atualizar_dados(
#    dados["selic"], dados["cambio"], dados["ipca"]
#)

# Agora você pode acessar os DataFrames atualizados:
#df_selic = dados_atualizados["selic"]
#df_cambio = dados_atualizados["cambio"]
#df_ipca = dados_atualizados["ipca"]

#Para ver
#df_ipca
#df_cambio
#df_selic

# 3. Exemplo: filtrar dados de câmbio para Março de 2024
#df_filtrado = filtrar_por_ano_mes(df_cambio, "2024", "março")

# 4. Ver os dados
#print(df_filtrado)