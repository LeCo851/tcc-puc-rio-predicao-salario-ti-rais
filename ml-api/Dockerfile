FROM python:3.11-slim

# Define o diretório de trabalho principal
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# --- AJUSTE DE SEGURANÇA DE MEMÓRIA ---
# Isso impede que o Python "fragmente" a memória e estoure os 512MB
ENV MALLOC_ARENA_MAX=2
# Isso impede que bibliotecas como Numpy/Pandas tentem usar todos os cores (o que gasta mais RAM)
ENV OMP_NUM_THREADS=1

# 1. Copia o requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copia a pasta app
COPY ./app ./app

# 3. Muda o diretório
WORKDIR /app/app

# Expõe a porta
EXPOSE 8000

# Executa
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]