# main.py
from fastapi import FastAPI
from routes import router

# Inicializa a aplicação FastAPI com um título personalizado
app = FastAPI(title="API IPEA - Relatórios Inteligentes")

# Inclui as rotas definidas no arquivo routes.py
app.include_router(router)

