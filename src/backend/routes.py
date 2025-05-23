from fastapi import APIRouter, HTTPException, Query
from utils.dados import (
    carregar_dados, 
    atualizar_dados, 
    filtrar_por_ano_mes, 
    media_mensal, 
    media_anual
)
from nlp import gerar_analises
from utils.alertas import gerar_alertas

router = APIRouter()

# Carrega e atualiza os dados
dados = carregar_dados()
if dados:
    dados = atualizar_dados(dados)
else:
    raise RuntimeError("Não foi possível carregar os dados iniciais.")

# Rotas para todos os dados disponíveis
@router.get("/{tipo}")
def get_dado(tipo: str):
    if tipo not in dados:
        raise HTTPException(status_code=404, detail=f"Tipo '{tipo}' não encontrado.")
    return dados[tipo].to_dict(orient="records")

# Filtro por ano e mês
@router.get("/filtro/{tipo}")
def get_filtrado(tipo: str, ano: str = Query(...), mes: str = Query(...)):
    if tipo not in dados:
        raise HTTPException(status_code=400, detail="Tipo inválido.")
    df = dados[tipo]
    filtrado = filtrar_por_ano_mes(df, ano, mes)
    return filtrado.to_dict(orient="records")

# Média mensal
@router.get("/media_mensal/{tipo}")
def get_media_mensal(tipo: str, ano: str = Query(...), mes: str = Query(...)):
    if tipo not in dados:
        raise HTTPException(status_code=400, detail="Tipo inválido.")
    resultado = media_mensal(dados[tipo], ano, mes)
    return {"tipo": tipo, "ano": ano, "mes": mes, "media_mensal": resultado}

# Média anual
@router.get("/media_anual/{tipo}")
def get_media_anual(tipo: str, ano: str = Query(...)):
    if tipo not in dados:
        raise HTTPException(status_code=400, detail="Tipo inválido.")
    resultado = media_anual(dados[tipo], ano)
    return {"tipo": tipo, "ano": ano, "media_anual": resultado}

# Análises de NLP
@router.get("/previsao")
def previsoes():
    return gerar_analises()

# Geração de alertas
@router.get("/alertas")
def rota_alertas():
    lista_de_alertas = gerar_alertas(dados)
    return {"alertas": lista_de_alertas}
