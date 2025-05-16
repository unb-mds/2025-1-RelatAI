from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from utils.dados import carregar_dados, atualizar_dados
from utils.dados import df_cambio, df_ipca, df_selic, filtrar_por_ano_mes
from utils.alertas import gerar_alertas
from ml import aplicar_modelo_tendencia
from nlp import gerar_resumo_nlp

router = APIRouter()

