export interface DadosProfissional {
  cargo: string;
  idade: number;
  escolaridade: string;
  uf: string;
  sexo: string;
  raca: string;
  tamanho_empresa: string;
  setor: string;
  ano_referencia: number;
}

export interface PrevisaoSalario {
  resultado: {
    cargo_selecionado: string;
    salario_estimado: string;
    detalhes_perfil: {
      porte_empresa: string;
      setor_atuacao: string;
    }
  };
  status: string;
}
