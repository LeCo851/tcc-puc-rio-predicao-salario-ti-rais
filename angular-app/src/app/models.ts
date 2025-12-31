export interface DadosProfissional {
  cargo: string;
  idade: number | null;
  faixa_experiencia?: string;
  escolaridade: string;
  uf: string;
  sexo: string;
  raca: string;
  tamanho_empresa: string;
  setor: string;
  ano_referencia: number;
}
export interface DetalhesPerfil {

  porteEmpresa: string;
  escolaridade: string;
  nivelExperiencia: string;
  raca: string; // Adicionado
}

export interface ResultadoDTO {
  // --- DADOS NUMÉRICOS (Vindos do Python) ---
  salario_estimado: number;
  faixa_confianca_min: number;
  faixa_confianca_max: number;

  // --- DADOS FORMATADOS (Vindos do Java) ---
  salario_corrigido: string;       // "R$ 7.500,00"
  salarioMinFormatado: string;    // "R$ 5.000,00"
  salarioMaxFormatado: string;    // "R$ 10.000,00"

  fator_correcao: number;
  cargo: string;

  // Objeto aninhado com os detalhes
  detalhesPerfil: DetalhesPerfil;
}

export interface PrevisaoSalario {
  cargo: string;      // Agora está na raiz
  mensagem: string;   // Substituiu o antigo 'status'
  resultado: ResultadoDTO;

}
