FROM python:3.10-slim
WORKDIR /app

# Copia o requirements.txt que está em 'src/'
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo da pasta 'src/backend' para o contêiner
COPY src/backend/ .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]