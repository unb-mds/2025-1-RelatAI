from fastapi import APIRouter
from utils.dados import carregar_dados, baixar_dados_banco_central
from utils.alertas import gerar_alertas
from ml import aplicar_modelo_tendencia
from nlp import gerar_resumo_nlp

router = APIRouter()

# Endpoint que retorna dados do CSV local
@router.get("/api/dados")
def get_dados():
    df = carregar_dados()
    return df.to_dict(orient="records")

# Endpoint que retorna dados atualizados direto da API do Banco Central
@router.get("/api/dados_atualizados")
def get_dados_atualizados():
    df = baixar_dados_banco_central()
    return df.to_dict(orient="records")

# Endpoint que retorna alertas financeiros com base em médias anuais
@router.get("/api/alertas")
def get_alertas():
    alertas = gerar_alertas()
    return alertas

# Endpoint que retorna resumo de tópicos utilizando modelo de NLP
@router.get("/api/resumo")
def get_resumo():
    texto = gerar_resumo_nlp()
    return {"resumo": texto}

# Endpoint que retorna previsão de tendência financeira para o próximo ano
@router.get("/api/tendencia")
def get_tendencia():
    valor_previsto = aplicar_modelo_tendencia()
    return {"previsao_proximo_ano": valor_previsto}