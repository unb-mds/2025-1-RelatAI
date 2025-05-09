import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.dados import carregar_dados

# Aplica um modelo de regressão linear para prever o valor financeiro do próximo ano
def aplicar_modelo_tendencia():
    df = carregar_dados()
    df = df.groupby("ano")["valor"].sum().reset_index()  # Soma valores por ano
    X = df[["ano"]]  # Variável independente
    y = df["valor"]   # Variável dependente
    modelo = LinearRegression()
    modelo.fit(X, y)  # Treina o modelo
    tendencia_ano_seguinte = modelo.predict([[df["ano"].max() + 1]])
    return tendencia_ano_seguinte[0]
