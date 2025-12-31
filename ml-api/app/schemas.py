from pydantic import BaseModel, Field
from typing import List, Optional
from enums import CargoEnum, TamanhoEmpresaEnum, EscolaridadeEnum, SexoEnum, RacaEnum, FaixaExperienciaEnum, SetorIbgeEnum

# --- DTOs de Entrada ---

class DadosProfissional(BaseModel):
    """Modelo usado para o endpoint /predict (Individual)"""
    cargo: CargoEnum = Field(..., description="Cargo do profissional")
    
    # ADICIONADO ALIAS AQUI (O Java manda 'tamanhoEmpresa')
    tamanho_empresa: TamanhoEmpresaEnum = Field(..., description="Porte da empresa", alias="tamanhoEmpresa")
    
    escolaridade: EscolaridadeEnum = Field(..., description="Grau de instrução")
    setor: SetorIbgeEnum = Field(..., description="Setor de atuação da empresa")
    uf: str = Field(..., min_length=2, max_length=2, description="Sigla do Estado (ex: SP)",examples=["SP", "RJ", "MG"])
    
    # CORRIGIDO: O Java manda 'anoReferencia' (CamelCase), não 'ano_referencia'
    ano: int = Field(default=2024, alias="anoReferencia", description="Ano de referência")
    
    idade: int | None = Field(default=None, ge=18, le=80, description="Idade em anos")
    
    # ESTE É O CAMPO CRÍTICO:
    # O Java manda "faixaExperiencia". O alias garante que o Python leia corretamente.
    faixa_experiencia: FaixaExperienciaEnum | None = Field(
        default=None, 
        alias="faixaExperiencia", 
        description="Nível de Senioridade"
    )
    
    sexo: SexoEnum = Field(default=SexoEnum.MASCULINO)
    raca: RacaEnum = Field(default=RacaEnum.BRANCA)

    # --- CORREÇÃO IMPORTANTE: A Config deve ficar DENTRO da classe ---
    class Config:
        populate_by_name = True

class SolicitacaoMapa(BaseModel):
    """Modelo usado para o endpoint /analise/mapa (Batch)"""
    cargo: CargoEnum = Field(..., description="Cargo para análise")
    
    # CORRIGIDO ALIAS
    ano: int = Field(default=2024, alias="anoReferencia", description="Ano de referência")
    
    idade: int | None = Field(default=None)
    
    # CORRIGIDO ALIAS
    faixa_experiencia: FaixaExperienciaEnum | None = Field(default=None, alias="faixaExperiencia")
    
    escolaridade: EscolaridadeEnum = Field(default=EscolaridadeEnum.SUPERIOR_COMPLETO)
    
    # CORRIGIDO ALIAS
    tamanho_empresa: TamanhoEmpresaEnum = Field(default=TamanhoEmpresaEnum.DE_100_A_249, alias="tamanhoEmpresa")
    
    setor: SetorIbgeEnum = Field(default=SetorIbgeEnum.INST_FINANCEIRAS)
    sexo: SexoEnum = Field(default=SexoEnum.MASCULINO)
    raca: RacaEnum = Field(default=RacaEnum.BRANCA)

    # --- CORREÇÃO IMPORTANTE: A Config deve ficar DENTRO da classe ---
    class Config:
        populate_by_name = True

# --- DTOs de Saída ---

class ResultadoSalario(BaseModel):
    salario_estimado: float
    faixa_confianca_min: float
    faixa_confianca_max: float

class PredictResponse(BaseModel):
    cargo: str
    resultado: ResultadoSalario
    mensagem: str