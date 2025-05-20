import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime
from utils.dados import carregar_dados

def preparar_dados(df):
    df = df.copy()
    df['data'] = pd.to_datetime(df['data'], format="%d-%m-%Y")
    df = df.sort_values("data")
    df['valor'] = df['valor'].astype(str).str.replace(",", ".").astype(float)
    df['timestamp'] = df['data'].map(datetime.toordinal)
    # Suaviza para reduzir ruídos
    df['valor_suave'] = df['valor'].rolling(window=5).mean().fillna(method='bfill')
    return df

def prever_tendencia(df, nome_serie):
    df = preparar_dados(df)
    X = df[['timestamp']]
    y = df['valor_suave']  # usando suavizado

    modelo = LinearRegression()
    modelo.fit(X, y)

    ultima_data = df['data'].max()
    futura_data = ultima_data.toordinal() + 30  # 30 dias após último dado

    previsao = modelo.predict([[futura_data]])[0]

    texto = (
        f"A série {nome_serie.upper()} tem uma tendência {'de alta' if modelo.coef_[0] > 0 else 'de baixa'} "
        f"com base nos dados históricos. A previsão para 30 dias após {ultima_data.strftime('%d-%m-%Y')} "
        f"é aproximadamente {previsao:.2f}."
    )

    return {
        "tendencia": "alta" if modelo.coef_[0] > 0 else "baixa",
        "previsao_30_dias": round(previsao, 2),
        "maior_valor": round(df['valor'].max(), 2),
        "menor_valor": round(df['valor'].min(), 2),
        "descricao": texto
    }


def gerar_analises():
    dados = carregar_dados()
    return {
        "selic": prever_tendencia(dados["selic"], "Selic"),
        "cambio": prever_tendencia(dados["cambio"], "Câmbio"),
        "ipca": prever_tendencia(dados["ipca"], "IPCA")
    }
