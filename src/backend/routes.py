from fastapi import FastAPI, HTTPException, Query, APIRouter
from utils.dados import carregar_dados, atualizar_dados, filtrar_por_ano_mes
from nlp import gerar_analises
from utils.alertas import *

router = APIRouter()

dados = carregar_dados()

if dados:
    dados = atualizar_dados(dados["selic"], dados["cambio"], dados["ipca"])
else:
    raise RuntimeError("Não foi possível carregar os dados iniciais.")

@router.get("/selic")
def get_selic():
    return dados["selic"].to_dict(orient="records")

@router.get("/cambio")
def get_cambio():
    return dados["cambio"].to_dict(orient="records")

@router.get("/ipca")
def get_ipca():
    return dados["ipca"].to_dict(orient="records")

@router.get("/filtro/{tipo}")
def get_filtrado(tipo: str, ano: str = Query(...), mes: str = Query(...)):
    if tipo not in ["selic", "cambio", "ipca"]:
        raise HTTPException(status_code=400, detail="Tipo deve ser: selic, cambio ou ipca")

    df = dados[tipo]
    filtrado = filtrar_por_ano_mes(df, ano, mes)
    return filtrado.to_dict(orient="records")

@router.get("/previsao")
def previsoes():
    return gerar_analises()

@router.get("/alertas")
def rota_alertas():
    dados = carregar_dados()
    lista_de_alertas = gerar_alertas(dados)
    return {"alertas": lista_de_alertas}