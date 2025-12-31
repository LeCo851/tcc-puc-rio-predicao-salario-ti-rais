FROM python:3.11-slim

# Define o diretório de trabalho principal
WORKDIR /app

# Instala dependências do sistema (libgomp1 é necessária para o XGBoost/LightGBM)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 1. Copia o requirements primeiro para aproveitar o cache das camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copia todo o conteúdo da sua pasta local 'app' para a pasta 'app' no container
# Isso já levará o app.py, service.py, enums.py, mappings.py, schemas.py, 
# o modelo .pkl e o arquivo .parquet de uma vez.
COPY ./app ./app

# 3. Muda o diretório de trabalho para dentro da pasta onde está o app.py
WORKDIR /app/app

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Executa o comando usando o módulo uvicorn
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]