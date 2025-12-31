import pandas as pd
import numpy as np

# 1. Carrega a base original
print("Carregando base bruta...")
df = pd.read_parquet(r"I:\Drive\MBA PUC\tcc-puc-rio-predicao-salario-ti-rais\ml-api\app\dados_rais_brutos.parquet")

# 2. Filtra apenas as colunas que seu service.py REALMENTE usa
cols_uteis = ['cbo_2002', 'sigla_uf', 'ano', 'sexo', 'idade']
df = df[cols_uteis]

# 3. Filtra apenas anos recentes (O Front mostra 2019 a 2024)
# Se sua base tiver 2010, 2015... isso está comendo memória à toa.
print("Filtrando anos...")
df = df[df['ano'] >= 2019]

# 4. Otimização Agressiva de Tipos (Downcasting)
print("Otimizando tipos...")
df['cbo_2002'] = df['cbo_2002'].astype('category')
df['sigla_uf'] = df['sigla_uf'].astype('category')

# Idade cabe em int8 (0 a 127)
df['idade'] = df['idade'].fillna(30).astype('int8')

# Sexo cabe em int8
df['sexo'] = df['sexo'].fillna(1).astype('int8')

# Ano cabe em int16
df['ano'] = df['ano'].astype('int16')

# 5. Salva a versão Lite
print(f"Salvando versão Lite... Linhas: {len(df)}")
df.to_parquet("dados_rais_lite.parquet", index=False)
print("Sucesso! Agora use 'dados_rais_lite.parquet' no seu sistema.")