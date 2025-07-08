FROM python:3.10-slim
WORKDIR /app

# Copia o requirements.txt que está em 'src/'
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo da pasta 'src/frontend' para o contêiner
COPY src/frontend/ .

EXPOSE 8501
CMD ["streamlit", "run", "Home.py", "--server.port", "8501", "--server.address", "0.0.0.0"]