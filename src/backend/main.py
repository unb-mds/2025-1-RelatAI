from fastapi import FastAPI
from routes import router as api_router


app = FastAPI(title="Minha API")

app.include_router(api_router)  # Conecta todas as rotas
