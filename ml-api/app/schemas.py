from pydantic import BaseModel, Field
from enums import CargoEnum, EscolaridadeEnum, TamanhoEmpresaEnum, SetorIbgeEnum, SexoEnum, RacaEnum

class DadosProfissional(BaseModel):
    cargo: CargoEnum = Field(..., description="Selecione o cargo na lista", example="Analista de desenvolvimento de sistemas")
    idade: int = Field(..., ge=14, le=100, description="Idade em anos", example=30)
    escolaridade: EscolaridadeEnum = Field(..., description="Nível de escolaridade", example="Superior Completo")
    tamanho_empresa: TamanhoEmpresaEnum = Field(..., description="Porte da empresa contratante", example="De 50 a 99 funcionários")
    setor: SetorIbgeEnum = Field(..., description="Setor de atuação da empresa", example="Instituições Financeiras (Bancos)")
    uf: str = Field(..., min_length=2, max_length=2, description="Sigla do Estado (Ex: SP, RJ)", example="SP")
    sexo: SexoEnum = Field(..., description="Gênero", example="Masculino")
    raca: RacaEnum = Field(..., description="Autodeclaração de raça/cor", example="Branca")
    ano_referencia: int = Field(default=2024, description="Ano para previsão (padrão atual)")
    
    
class SolicitacaoMapa(BaseModel):
    cargo: CargoEnum = Field(..., description="Cargo para análise geográfica", example="Cientista de dados")
    ano: int = Field(default=2024, ge=2019, le=2024, description="Ano de referência", example=2024)
    
    # Filtros Opcionais (Com valores padrão de mercado)
    idade: int = Field(default=30, ge=16, le=70, description="Idade para simulação")
    sexo: SexoEnum = Field(default=SexoEnum.MASCULINO, description="Gênero para simulação")
    raca: RacaEnum = Field(default=RacaEnum.BRANCA, description="Raça/Cor para simulação")
    tamanho_empresa: TamanhoEmpresaEnum = Field(default=TamanhoEmpresaEnum.DE_50_A_99, description="Porte da empresa")
    escolaridade: EscolaridadeEnum = Field(default=EscolaridadeEnum.SUPERIOR_COMPLETO, description="Nível de instrução")
    setor: SetorIbgeEnum = Field(default=SetorIbgeEnum.INST_FINANCEIRAS, description="Setor de atuação")  