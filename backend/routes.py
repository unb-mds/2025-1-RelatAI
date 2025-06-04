from fastapi import FastAPI, HTTPException, Query, APIRouter, Body
from .utils.dados import carregar_dados, atualizar_dados, filtrar_por_ano_mes, filtrar_pib_por_ano_trimestre
from .utils.alertas import *
from frontend.utils.ml_models import predict_future_values # Importar a função do novo local
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

dados = carregar_dados()

if dados:
    # Atualização para incluir o PIB
    dados = atualizar_dados(dados["selic"], dados["cambio"], dados["ipca"], dados["pib"], dados["divida"], dados["desemprego"])
else:
    raise RuntimeError("Não foi possível carregar os dados iniciais.")

class PredictionRequest(BaseModel):
    historical_data: List[Dict[str, Any]]
    periods: int = 90
    window_size: int = 15
    model_type: str = "deepseek"

@router.get("/selic")
def get_selic():
    return dados["selic"].to_dict(orient="records")

@router.get("/cambio")
def get_cambio():
    return dados["cambio"].to_dict(orient="records")

@router.get("/ipca")
def get_ipca():
    return dados["ipca"].to_dict(orient="records")

@router.get("/pib")
def get_pib():
    return dados["pib"].to_dict(orient="records")

@router.get("/divida")
def get_divida():
    return dados["divida"].to_dict(orient="records")

@router.get("/desemprego")
def get_desemprego():
    return dados["desemprego"].to_dict(orient="records")

@router.get("/filtro/{tipo}")
def get_filtrado(tipo: str, ano: str = Query(...), mes: str = Query(...)):
    if tipo not in ["selic", "cambio", "ipca", "pib", "divida", "desemprego"]:  
        raise HTTPException(status_code=400, detail="Tipo deve ser: selic, cambio, ipca, pib, divida ou desemprego")

    if tipo == "pib":
        # PIB deve usar trimestre em vez de mês
        raise HTTPException(status_code=400, detail="Para dados do PIB, use a rota /filtro-pib/{ano}/{trimestre}")
    
    df = dados[tipo]
    filtrado = filtrar_por_ano_mes(df, ano, mes)
    return filtrado.to_dict(orient="records")

# Nova rota específica para filtrar PIB por trimestre
@router.get("/filtro-pib/{ano}")
def get_pib_filtrado(ano: str, trimestre: Optional[str] = Query(None)):
    """
    Filtra os dados do PIB por ano e trimestre.
    Se o trimestre não for fornecido, retorna todos os trimestres do ano.
    """
    df = dados["pib"]
    filtrado = filtrar_pib_por_ano_trimestre(df, ano, trimestre)
    
    if filtrado.empty:
        raise HTTPException(status_code=404, detail=f"Dados não encontrados para o ano {ano} e trimestre {trimestre}")
        
    return filtrado.to_dict(orient="records")

@router.post("/predict/{indicator_name}")
async def predict_indicator(indicator_name: str, request: PredictionRequest):
    """
    Gera previsões para um indicador econômico
    """
    # Validar se o indicator_name é válido
    if indicator_name.lower() not in ["selic", "cambio", "ipca", "pib", "divida", "desemprego"]:
        raise HTTPException(status_code=400, detail="Indicador deve ser: selic, cambio, ipca, pib, divida ou desemprego")

    try:
        # Verificar se há dados históricos suficientes
        if len(request.historical_data) < request.window_size * 2:
            raise HTTPException(
                status_code=400, 
                detail=f"Dados históricos insuficientes para análise de {indicator_name.upper()}. Necessários pelo menos {request.window_size * 2} pontos."
            )
            
        forecast_df = predict_future_values(
            request.historical_data,
            periods=request.periods,
            window_size=request.window_size,
            model_type=request.model_type
        )
        
        if forecast_df is None:
            raise HTTPException(status_code=400, detail="Não foi possível gerar previsões")
            
        result = forecast_df.copy()
        result['data'] = result['data'].dt.strftime('%Y-%m-%d')
        
        return result.to_dict(orient='records')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar previsão: {str(e)}")

@router.get("/alertas")
def rota_alertas():
    # Carregar dados frescos para os alertas
    dados_frescos = carregar_dados()
    if not dados_frescos:
        raise HTTPException(status_code=500, detail="Erro ao carregar dados para alertas")
        
    lista_de_alertas = gerar_alertas(dados_frescos)
    return {"alertas": lista_de_alertas}