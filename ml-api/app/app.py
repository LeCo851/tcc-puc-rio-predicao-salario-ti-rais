from fastapi import FastAPI, HTTPException
from schemas import DadosProfissional, SolicitacaoMapa
from service import salario_service 

app = FastAPI(
    title="API de Inferência Salarial - Data Science",
    description="Prevê salários de TI com base em dados históricos da RAIS.",
    version="1.0"
)

@app.post("/predict", summary="Calcular estimativa salarial")
def prever_salario(dados: DadosProfissional):
    try:
        # Chamamos o service que contém toda a lógica suja
        salario_reais = salario_service.prever(dados)

        return {
            "resultado": {
                "cargo_selecionado": dados.cargo.value,
                "salario_estimado": f"R$ {round(salario_reais, 2):.2f}".replace('.', ','),
                "detalhes_perfil": {
                    "porte_empresa": dados.tamanho_empresa.value,
                    "setor_atuacao": dados.setor.value
                }
            },
            "status": "sucesso"
        }

    except Exception as e:
        print(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao calcular salário.")

@app.post("/analise/mapa", summary="Dados para o Mapa de Calor", response_model=list[dict])
def dados_mapa(dados: SolicitacaoMapa):
    try:
        # AGORA PASSAMOS O ANO TAMBÉM
        resultado = salario_service.gerar_dados_mapa(dados)
        
        if not resultado:
            return []
            
        return resultado
    except Exception as e:
        print(f"Erro no mapa: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar dados: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)