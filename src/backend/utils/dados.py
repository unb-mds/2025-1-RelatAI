import pandas as pd
import requests
from io import StringIO

# URLs das APIs do Banco Central
URL_SELIC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv&dataInicial=12/05/2016"
URL_CAMBIO = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial=12/05/2016"
URL_IPCA = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv"
URL_PIB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4380/dados?formato=csv&dataInicial=01/01/2010"

# Função para carregar os dados diretamente da API
def carregar_dados():
    try:
        # Baixar dados diretamente (sem tratamento)
        response_selic = requests.get(URL_SELIC)
        response_cambio = requests.get(URL_CAMBIO)
        response_ipca = requests.get(URL_IPCA)
        response_pib = requests.get(URL_PIB)

        # Verifica se as requisições foram bem-sucedidas
        if (response_selic.status_code == 200 and 
            response_cambio.status_code == 200 and 
            response_ipca.status_code == 200 and
            response_pib.status_code == 200):
            
            # Converter respostas em DataFrame bruto
            df_selic = pd.read_csv(StringIO(response_selic.text), sep=";", decimal=".")
            df_cambio = pd.read_csv(StringIO(response_cambio.text), sep=";", decimal=".")
            df_ipca = pd.read_csv(StringIO(response_ipca.text), sep=";", decimal=".")
            df_pib = pd.read_csv(StringIO(response_pib.text), sep=";", decimal=".")
            
            # transformar coluna data para tipo datetime em pandas
            df_ipca['data'] = pd.to_datetime(df_ipca['data'], format="%d/%m/%Y")
            df_cambio['data'] = pd.to_datetime(df_cambio['data'], format="%d/%m/%Y")
            df_selic['data'] = pd.to_datetime(df_selic['data'], format="%d/%m/%Y")
            df_pib['data'] = pd.to_datetime(df_pib['data'], format="%d/%m/%Y")

            # criando coluna mês e ano
            df_cambio['mes'] = df_cambio['data'].dt.month_name()
            df_ipca['mes'] = df_ipca['data'].dt.month_name()
            df_selic['mes'] = df_selic['data'].dt.month_name()
            df_pib['mes'] = df_pib['data'].dt.month_name()

            df_cambio['ano'] = df_cambio['data'].dt.year.astype(str)
            df_ipca['ano'] = df_ipca['data'].dt.year.astype(str)
            df_selic['ano'] = df_selic['data'].dt.year.astype(str)
            df_pib['ano'] = df_pib['data'].dt.year.astype(str)
            
            # Adicionar coluna de trimestre para o PIB
            df_pib['trimestre'] = df_pib['data'].dt.quarter.astype(str)

            for df in [df_selic, df_cambio, df_ipca, df_pib]:
                df['data'] = df['data'].dt.strftime('%d-%m-%Y')

            return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca, "pib": df_pib}
        else:
            raise Exception("Erro ao acessar as APIs do Banco Central.")
    except Exception as e:
        print(f"Erro ao carregar dados da API: {e}")
        return None

from datetime import timedelta

# Função para atualizar os DataFrames existentes com novos dados da API
def atualizar_dados(df_selic, df_cambio, df_ipca, df_pib):
    try:
        # Converter strings de data para datetime para processamento
        if isinstance(df_selic['data'].iloc[0], str):
            df_selic['data'] = pd.to_datetime(df_selic['data'], format='%d-%m-%Y')
        if isinstance(df_cambio['data'].iloc[0], str):
            df_cambio['data'] = pd.to_datetime(df_cambio['data'], format='%d-%m-%Y')
        if isinstance(df_ipca['data'].iloc[0], str):
            df_ipca['data'] = pd.to_datetime(df_ipca['data'], format='%d-%m-%Y')
        if isinstance(df_pib['data'].iloc[0], str):
            df_pib['data'] = pd.to_datetime(df_pib['data'], format='%d-%m-%Y')
            
        # Obtém a última data de cada DataFrame
        ultima_data_selic = df_selic['data'].max()
        ultima_data_cambio = df_cambio['data'].max()
        ultima_data_ipca = df_ipca['data'].max()
        ultima_data_pib = df_pib['data'].max()

        # Define a data inicial para a próxima consulta (um dia após o último dado)
        data_inicial_selic = (ultima_data_selic + timedelta(days=1)).strftime("%d/%m/%Y")
        data_inicial_cambio = (ultima_data_cambio + timedelta(days=1)).strftime("%d/%m/%Y")
        data_inicial_ipca = (ultima_data_ipca + timedelta(days=1)).strftime("%d/%m/%Y")
        data_inicial_pib = (ultima_data_pib + timedelta(days=1)).strftime("%d/%m/%Y")

        data_final = pd.Timestamp.today().strftime("%d/%m/%Y")

        # URLs com intervalo atualizado
        url_selic = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv&dataInicial={data_inicial_selic}&dataFinal={data_final}"
        url_cambio = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial={data_inicial_cambio}&dataFinal={data_final}"
        url_ipca = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv&dataInicial={data_inicial_ipca}&dataFinal={data_final}"
        url_pib = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4380/dados?formato=csv&dataInicial={data_inicial_pib}&dataFinal={data_final}"

        # Requisições
        response_selic = requests.get(url_selic)
        response_cambio = requests.get(url_cambio)
        response_ipca = requests.get(url_ipca)
        response_pib = requests.get(url_pib)

        # Verificação para SELIC, CÂMBIO e IPCA (como já estava)
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
        
        # Nova verificação para o PIB
        if response_pib.status_code == 200:
            novos_dados_pib = pd.read_csv(StringIO(response_pib.text), sep=";", decimal=",")
            if not novos_dados_pib.empty:
                novos_dados_pib['data'] = pd.to_datetime(novos_dados_pib['data'], format="%d/%m/%Y")
                novos_dados_pib['mes'] = novos_dados_pib['data'].dt.month_name()
                novos_dados_pib['ano'] = novos_dados_pib['data'].dt.year.astype(str)
                novos_dados_pib['trimestre'] = novos_dados_pib['data'].dt.quarter.astype(str)
                df_pib = pd.concat([df_pib, novos_dados_pib]).drop_duplicates(subset='data')
        
        # Converter datas de volta para string no formato consistente
        for df in [df_selic, df_cambio, df_ipca, df_pib]:
            if not isinstance(df['data'].iloc[0], str):
                df['data'] = df['data'].dt.strftime('%d-%m-%Y')
                
        # Retorna todos os DataFrames atualizados
        return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca, "pib": df_pib}

    except Exception as e:
        print(f"Erro ao atualizar os dados: {e}")
        # Converter datas de volta para string se necessário
        for df in [df_selic, df_cambio, df_ipca, df_pib]:
            if not isinstance(df['data'].iloc[0], str):
                df['data'] = df['data'].dt.strftime('%d-%m-%Y')
        return {"selic": df_selic, "cambio": df_cambio, "ipca": df_ipca, "pib": df_pib}


# Função de filtro por ano e mês
def filtrar_por_ano_mes(df, ano: str, mes: str):
    return df[(df['ano'] == ano) & (df['mes'].str.lower() == mes.lower())]



# Função para filtrar dados do PIB por ano e trimestre
def filtrar_pib_por_ano_trimestre(df_pib, ano: str, trimestre: str = None):
    """
    Filtra os dados do PIB por ano e, opcionalmente, por trimestre
    
    Args:
        df_pib: DataFrame com dados do PIB
        ano: Ano desejado como string (ex: "2023")
        trimestre: Trimestre desejado como string (ex: "1", "2", "3", "4") ou None para todos
        
    Returns:
        DataFrame filtrado
    """
    if trimestre is None:
        return df_pib[df_pib['ano'] == ano]
    else:
        return df_pib[(df_pib['ano'] == ano) & (df_pib['trimestre'] == trimestre)]


## 1. Carregar os dados iniciais
# dados = carregar_dados()

# 2. Atualizar os dados até a data atual
# dados_atualizados = atualizar_dados(
#    dados["selic"], dados["cambio"], dados["ipca"], dados["pib"]
# )

# Agora você pode acessar os DataFrames atualizados:
# df_selic = dados_atualizados["selic"]
# df_cambio = dados_atualizados["cambio"]
# df_ipca = dados_atualizados["ipca"]
# df_pib = dados_atualizados["pib"]

# 3. Exemplo: filtrar dados do PIB para 2023, primeiro trimestre
# pib_2023_t1 = filtrar_pib_por_ano_trimestre(df_pib, "2023", "1")

# 4. Ver os dados
# print(pib_2023_t1)