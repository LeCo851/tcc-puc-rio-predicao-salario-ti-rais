import pandas as pd
import numpy as np
import joblib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

# ==============================================================================
# 1. ENUMS (OPÇÕES EM LINGUAGEM NATURAL PARA O USUÁRIO)
# ==============================================================================

class EscolaridadeEnum(str, Enum):
    ANALFABETO = "Analfabeto"
    FUNDAMENTAL_INCOMPLETO = "Fundamental Incompleto"
    FUNDAMENTAL_COMPLETO = "Fundamental Completo"
    MEDIO_INCOMPLETO = "Médio Incompleto"
    MEDIO_COMPLETO = "Médio Completo"
    SUPERIOR_INCOMPLETO = "Superior Incompleto"
    SUPERIOR_COMPLETO = "Superior Completo"
    MESTRADO = "Mestrado"
    DOUTORADO = "Doutorado"

class SexoEnum(str, Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"

class RacaEnum(str, Enum):
    INDIGENA = "Indígena"
    BRANCA = "Branca"
    PRETA = "Preta"
    AMARELA = "Amarela"
    PARDA = "Parda"
    NAO_INFORMADO = "Não Informado"

class TamanhoEmpresaEnum(str, Enum):
    ZERO = "Zero funcionários"
    ATE_4 = "De 1 a 4 funcionários"
    DE_5_A_9 = "De 5 a 9 funcionários"
    DE_10_A_19 = "De 10 a 19 funcionários"
    DE_20_A_49 = "De 20 a 49 funcionários"
    DE_50_A_99 = "De 50 a 99 funcionários"
    DE_100_A_249 = "De 100 a 249 funcionários"
    DE_250_A_499 = "De 250 a 499 funcionários"
    DE_500_A_999 = "De 500 a 999 funcionários"
    MAIS_DE_1000 = "1000 ou mais funcionários"

class SetorIbgeEnum(str, Enum):
    EXTRA_MINERAL = "Extrativa Mineral" # 1
    IND_METALURGICA = "Indústria Metalúrgica" # 2
    IND_MECANICA = "Indústria Mecânica" # 3
    IND_ELETRICA = "Indústria Elétrica e Comunicação" # 4
    IND_TRANSPORTE = "Material de Transporte" # 5
    IND_MADEIRA_MOB = "Madeira e Mobiliário" # 6
    IND_PAPEL_GRAF = "Papel, Papelão e Gráfica" # 7
    IND_BORRACHA_COURO = "Borracha, Fumo, Couros" # 8
    IND_QUIMICA = "Indústria Química" # 9
    IND_TEXTIL = "Indústria Têxtil" # 10
    IND_CALCADOS = "Indústria de Calçados" # 11
    IND_ALIMENTOS = "Alimentos e Bebidas" # 12
    SERV_UTIL_PUB = "Serviços de Utilidade Pública" # 13
    CONSTRUCAO_CIVIL = "Construção Civil" # 14
    COMERCIO_VAREJISTA = "Comércio Varejista" # 15
    COMERCIO_ATACADISTA = "Comércio Atacadista" # 16
    INST_FINANCEIRAS = "Instituições Financeiras (Bancos)" # 17
    ADM_IMOVEIS = "Adm de Imóveis e Valores Mob." # 18
    TRANSPORTES = "Transportes e Comunicações" # 19
    SERV_ALOJ_ALIM = "Alojamento e Alimentação" # 20
    SERV_MEDICOS = "Médicos, Odontológicos e Veterinários" # 21
    ENSINO = "Ensino" # 22
    ADM_PUBLICA = "Administração Pública" # 23
    AGRICULTURA = "Agricultura e Pesca" # 24 e 25

class CargoEnum(str, Enum):
    ADMINISTRADOR_DE_BANCO_DE_DADOS = "Administrador de banco de dados"
    ADMINISTRADOR_DE_REDES = "Administrador de redes"
    ADMINISTRADOR_DE_SISTEMAS_OPERACIONAIS = "Administrador de sistemas operacionais"
    ADMINISTRADOR_EM_SEGURANÇA_DA_INFORMAÇÃO = "Administrador em segurança da informação"
    ANALISTA_DE_DESENVOLVIMENTO_DE_SISTEMAS = "Analista de desenvolvimento de sistemas"
    ANALISTA_DE_PESQUISA_DE_MERCADO = "Analista de pesquisa de mercado"
    ANALISTA_DE_REDES_E_DE_COMUNICAÇÃO_DE_DADOS = "Analista de redes e de comunicação de dados"
    ANALISTA_DE_SISTEMAS_DE_AUTOMAÇÃO = "Analista de sistemas de automação"
    ANALISTA_DE_SUPORTE_COMPUTACIONAL = "Analista de suporte computacional"
    ANALISTA_DE_TESTES_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Analista de testes de tecnologia da informação"
    ARQUITETO_DE_SOLUÇÕES_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Arquiteto de soluções de tecnologia da informação"
    CIENTISTA_DE_DADOS = "Cientista de dados"
    DESENHISTA_INDUSTRIAL_GRÁFICO_DESIGNER_GRÁFICO = "Desenhista industrial gráfico (designer gráfico)"
    DESENVOLVEDOR_DE_SISTEMAS_DE_TECNOLOGIA_DA_INFORMAÇÃO_TÉCNICO = "Desenvolvedor de sistemas de tecnologia da informação (técnico)"
    DIRETOR_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Diretor de tecnologia da informação"
    ENGENHEIRO_DE_APLICATIVOS_EM_COMPUTAÇÃO = "Engenheiro de aplicativos em computação"
    ENGENHEIRO_DE_EQUIPAMENTOS_EM_COMPUTAÇÃO = "Engenheiro de equipamentos em computação"
    ENGENHEIROS_DE_SISTEMAS_OPERACIONAIS_EM_COMPUTAÇÃO = "Engenheiros de sistemas operacionais em computação"
    ESPECIALISTA_EM_PESQUISA_OPERACIONAL = "Especialista em pesquisa operacional"
    ESTATÍSTICO = "Estatístico"
    ESTATÍSTICO_ESTATÍSTICA_APLICADA = "Estatístico (estatística aplicada)"
    ESTATÍSTICO_TEÓRICO = "Estatístico teórico"
    GERENTE_DE_INFRAESTRUTURA_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Gerente de infraestrutura de tecnologia da informação"
    GERENTE_DE_OPERAÇÃO_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Gerente de operação de tecnologia da informação"
    GERENTE_DE_PROJETOS_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Gerente de projetos de tecnologia da informação"
    GERENTE_DE_SEGURANÇA_DA_INFORMAÇÃO = "Gerente de segurança da informação"
    GERENTE_DE_SUPORTE_TÉCNICO_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Gerente de suporte técnico de tecnologia da informação"
    PESQUISADOR_EM_CIÊNCIAS_DA_COMPUTAÇÃO_E_INFORMÁTICA = "Pesquisador em ciências da computação e informática"
    PROFESSOR_DE_COMPUTAÇÃO_NO_ENSINO_SUPERIOR = "Professor de computação (no ensino superior)"
    TECNÓLOGO_EM_GESTÃO_DA_TECNOLOGIA_DA_INFORMAÇÃO = "Tecnólogo em gestão da tecnologia da informação"
    TÉCNICO_DE_SUPORTE_AO_USUÁRIO_DE_TECNOLOGIA_DA_INFORMAÇÃO = "Técnico de suporte ao usuário de tecnologia da informação"

# ==============================================================================
# 2. MAPAS DE TRADUÇÃO (TEXTO -> CÓDIGO RAIS)
# ==============================================================================

# Converte o Texto legível para o Código Numérico que o modelo treinou
mapa_escolaridade = {
    "Analfabeto": 1,
    "Fundamental Incompleto": 2, # Abrange até 5a incomp
    "Fundamental Completo": 6,  
    "Médio Incompleto": 5,
    "Médio Completo": 7,
    "Superior Incompleto": 8,
    "Superior Completo": 9,
    "Mestrado": 10,
    "Doutorado": 11
}

mapa_tamanho = {
    "Zero funcionários": 1,
    "De 1 a 4 funcionários": 2,
    "De 5 a 9 funcionários": 3,
    "De 10 a 19 funcionários": 4,
    "De 20 a 49 funcionários": 5,
    "De 50 a 99 funcionários": 6,
    "De 100 a 249 funcionários": 7,
    "De 250 a 499 funcionários": 8,
    "De 500 a 999 funcionários": 9,
    "1000 ou mais funcionários": 10
}

mapa_setor = {
    "Extrativa Mineral": 1,
    "Indústria Metalúrgica": 2,
    "Indústria Mecânica": 3,
    "Indústria Elétrica e Comunicação": 4,
    "Material de Transporte": 5,
    "Madeira e Mobiliário": 6,
    "Papel, Papelão e Gráfica": 7,
    "Borracha, Fumo, Couros": 8,
    "Indústria Química": 9,
    "Indústria Têxtil": 10,
    "Indústria de Calçados": 11,
    "Alimentos e Bebidas": 12,
    "Serviços de Utilidade Pública": 13,
    "Construção Civil": 14,
    "Comércio Varejista": 15,
    "Comércio Atacadista": 16,
    "Instituições Financeiras (Bancos)": 17,
    "Adm de Imóveis e Valores Mob.": 18,
    "Transportes e Comunicações": 19,
    "Alojamento e Alimentação": 20,
    "Médicos, Odontológicos e Veterinários": 21,
    "Ensino": 22,
    "Administração Pública": 23,
    "Agricultura e Pesca": 25
}

mapa_sexo = {
    "Masculino": 1,
    "Feminino": 2
}

mapa_raca = {
    "Indígena": 1,
    "Branca": 2,
    "Preta": 4,
    "Amarela": 6,
    "Parda": 8,
    "Não Informado": 9
}

# ==============================================================================
# 3. CARREGAMENTO DOS ARTEFATOS
# ==============================================================================
diretorio_base = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_base, 'modelo_salario_ti.pkl')

print(f"[INIT] Carregando modelo de: {caminho_arquivo}")

try:
    pacote = joblib.load(caminho_arquivo)
    
    modelo = pacote['modelo']
    encoders = pacote['encoders']
    cbo_map = pacote['cbo_map']
    mapa_medias = pacote.get('mapa_medias', {}) 
    media_global = pacote.get('media_global', 3000.0)

    # Inverte o mapa CBO (Nome -> Código) para busca
    # Remove espaços extras e converte para string para garantir match
    nome_para_cbo = {str(v).strip(): str(k) for k, v in cbo_map.items()}

    print(f"[OK] Modelo carregado com sucesso.")

except Exception as e:
    raise RuntimeError(f"Falha crítica ao carregar modelo: {e}")

# ==============================================================================
# 4. ESTRUTURA DE DADOS DA REQUISIÇÃO
# ==============================================================================
class DadosProfissional(BaseModel):
    cargo: CargoEnum = Field(..., description="Selecione o cargo na lista",example="Analista de desenvolvimento de sistemas")
    idade: int = Field(..., ge=14, le=100, description="Idade em anos", example=30)
    escolaridade: EscolaridadeEnum = Field(..., description="Nível de escolaridade",example="Superior Completo")
    tamanho_empresa: TamanhoEmpresaEnum = Field(..., description="Porte da empresa contratante",example="De 50 a 99 funcionários")
    setor: SetorIbgeEnum = Field(..., description="Setor de atuação da empresa",example="Instituições Financeiras (Bancos)")
    uf: str = Field(..., min_length=2, max_length=2, description="Sigla do Estado (Ex: SP, RJ)", example="SP")
    sexo: SexoEnum = Field(..., description="Gênero", example="Masculino")
    raca: RacaEnum = Field(..., description="Autodeclaração de raça/cor",example="Branca")
    ano_referencia: int = Field(default=2024, description="Ano para previsão (padrão atual)")

# ==============================================================================
# 5. API
# ==============================================================================
app = FastAPI(
    title="API de Inferência Salarial - Data Science",
    description="Prevê salários de TI com base em dados históricos da RAIS.",
    version="1.0"
)

@app.post("/predict", summary="Calcular estimativa salarial")
def prever_salario(dados: DadosProfissional):
    try:
        # --- ETAPA 1: TRADUÇÃO (Natural -> Código RAIS) ---
        
        # Cargo: Busca o CBO pelo nome exato
        cbo_codigo = nome_para_cbo.get(dados.cargo.value)
        if not cbo_codigo:
            # Fallback de segurança se der erro no string matching
            cbo_codigo = "000000" 

        # Tamanho da Empresa
        cod_tamanho = mapa_tamanho.get(dados.tamanho_empresa.value, 6) # 6 é medio (50-99) default

        # Escolaridade
        cod_escolaridade = mapa_escolaridade.get(dados.escolaridade.value, 9) # 9 (Superior) default

        # Setor IBGE
        cod_setor = mapa_setor.get(dados.setor.value, 13) # 13 (Serviços) default

        # Sexo e Raça (Códigos RAIS puros)
        cod_sexo_rais = mapa_sexo.get(dados.sexo.value, 1)
        cod_raca_rais = mapa_raca.get(dados.raca.value, 2)


        # --- ETAPA 2: FEATURE ENGINEERING (Target Encoding) ---
        # Aqui convertemos os códigos RAIS (ex: 'SP', '9') para as MÉDIAS salariais que o modelo aprendeu
        
        # 1. CBO
        val_cbo = mapa_medias['cbo'].get(str(cbo_codigo), media_global)
        
        # 2. Escolaridade (Converter int para str se a chave do dict for str)
        val_esc = mapa_medias['esc'].get(str(cod_escolaridade), media_global)
        
        # 3. UF
        val_uf = mapa_medias['uf'].get(dados.uf.upper(), media_global)
        
        # 4. Tamanho da Empresa
        val_tam = mapa_medias['tam'].get(str(cod_tamanho), media_global)
        
        # 5. Setor
        val_setor = mapa_medias['setor'].get(str(cod_setor), media_global)

        # 6. Sexo e Raça (Label Encoding)
        try:
            val_sexo_encoded = encoders['sexo'].transform([str(cod_sexo_rais)])[0]
            val_raca_encoded = encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
        except:
            val_sexo_encoded, val_raca_encoded = 0, 0

        # --- ETAPA 3: PREVISÃO ---
        # Montar o DataFrame com EXATAMENTE as mesmas colunas do treino
        df_input = pd.DataFrame({
            'cbo_valor': [val_cbo],
            'idade': [dados.idade],
            'esc_valor': [val_esc],
            'uf_valor': [val_uf],
            'tam_valor': [val_tam],
            'setor_valor': [val_setor],
            'sexo': [val_sexo_encoded],
            'raca_cor_valor': [val_raca_encoded],
            'ano': [dados.ano_referencia]
        })

        # Predict (Log Scale)
        log_salario = modelo.predict(df_input)[0]
        
        # Reverter Log (Scale Real)
        salario_reais = np.expm1(log_salario)

        # --- ETAPA 4: RESPOSTA AMIGÁVEL ---
        return {
            "resultado": {
                "cargo_selecionado": dados.cargo.value,
                "salario_estimado": f"R$ {round(float(salario_reais), 2):.2f}".replace('.', ','),
                "detalhes_perfil": {
                    "porte_empresa": dados.tamanho_empresa.value,
                    "setor_atuacao": dados.setor.value
                }
            },
            "status": "sucesso"
        }

    except Exception as e:
        print(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao calcular salário. Verifique os parâmetros.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)