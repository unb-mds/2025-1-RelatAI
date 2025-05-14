from fastapi import APIRouter
from utils.dados import carregar_dados, baixar_dados_banco_central
from utils.dados import df_cambio, df_ipca, df_selic, filtrar_por_ano_mes
>>>>>>> efe836184675026bb939af1940b9b62911a1cdb9
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

# Endpoint IPCA
@router.get("/api/ipca")
def get_ipca(ano: str, mes: str):
    try:
        # Aplica o filtro usando a função filtrar_por_ano_mes
        df_filtrado = filtrar_por_ano_mes(df_ipca, ano, mes)
        return JSONResponse(content=df_filtrado.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao filtrar os dados: {str(e)}")

# Endpoint SELIC
@router.get("/api/selic")
def get_selic(ano: str, mes: str):
    try:
        # Aplica o filtro usando a função filtrar_por_ano_mes
        df_filtrado = filtrar_por_ano_mes(df_selic, ano, mes)
        return JSONResponse(content=df_filtrado.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao filtrar os dados: {str(e)}")

# Endpoint Câmbio
@router.get("/api/cambio")
def get_cambio(ano: str, mes: str):
    try:
        # Aplica o filtro usando a função filtrar_por_ano_mes
        df_filtrado = filtrar_por_ano_mes(df_cambio, ano, mes)
        return JSONResponse(content=df_filtrado.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao filtrar os dados: {str(e)}")

# Endpoint para pegar todos os dados do IPCA sem filtro (caso necessário)
@router.get("/api/ipca/all")
def get_all_ipca():
    return JSONResponse(content=df_ipca.to_dict(orient="records"))

# Endpoint para pegar todos os dados do Câmbio sem filtro (caso necessário)
@router.get("/api/cambio/all")
def get_all_cambio():
    return JSONResponse(content=df_cambio.to_dict(orient="records"))

# Endpoint para pegar todos os dados da SELIC sem filtro (caso necessário)
@router.get("/api/selic/all")
def get_all_selic():
    return JSONResponse(content=df_selic.to_dict(orient="records"))

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