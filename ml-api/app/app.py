from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from schemas import DadosProfissional, PredictResponse, ResultadoSalario, SolicitacaoMapa
from service import salario_service # Instância global criada no final do service.py

# Gerenciamento de ciclo de vida (opcional, mas boa prática)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # O service já carrega tudo no __init__, mas aqui poderíamos forçar recargas se necessário
    print("API Iniciada. Quartis globais e Modelo carregados.")
    yield
    print("API Encerrada.")

app = FastAPI(
    title="API de Predição Salarial - TCC",
    description="API para prever salários de TI usando XGBoost e dados da RAIS",
    version="2.0",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    """Verifica se a API está online."""
    return {"status": "online", "modelo_carregado": salario_service.modelo is not None}

@app.post("/predict", response_model=PredictResponse)
def prever_salario(dados: DadosProfissional):
    """
    Endpoint para prever o salário de um ÚNICO profissional.
    """
    try:
        # O service agora resolve a idade sozinho (manual ou via faixa)
        salario = salario_service.prever(dados)
        
        margem_erro = 0.35
        return PredictResponse(
            cargo=dados.cargo.value,
            resultado=ResultadoSalario(
                salario_estimado=round(salario, 2),
                faixa_confianca_min=round(salario * (1 - margem_erro), 2),
                faixa_confianca_max=round(salario * (1 + margem_erro), 2)
            ),
            mensagem="Previsão realizada com sucesso."
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

@app.post("/analise/mapa")
def gerar_mapa(dados: SolicitacaoMapa):
    """
    Endpoint para gerar dados para o MAPA (27 estados).
    Retorna lista com salário estimado e estatísticas demográficas.
    """
    try:
        resultado = salario_service.gerar_dados_mapa(dados)
        return resultado
    except Exception as e:
        print(f"Erro no mapa: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar mapa: {str(e)}")

# Se for rodar localmente para teste sem Docker
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)