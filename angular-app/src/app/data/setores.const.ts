// src/app/data/setores.const.ts

export interface OpcaoSetor {
  label: string;
  value: string;
}

export const LISTA_SETORES: OpcaoSetor[] = [
  { label: 'Instituições Financeiras (Bancos)', value: 'Instituiçoes de crédito, seguros e capitalizaçao' },
  { label: 'Tecnologia & Consultoria', value: 'Com. e administraçao de imóveis, valores mobiliários, serv. Técnico' },
  { label: 'Comércio Varejista', value: 'Comércio varejista' },
  { label: 'Comércio Atacadista', value: 'Comércio atacadista' },
  { label: 'Indústria Têxtil', value: 'Indústria têxtil do vestuário e artefatos de tecidos' },
  { label: 'Indústria Química / Farmacêutica', value: 'Ind. química de produtos farmacêuticos, veterinários, perfumaria' },
  { label: 'Construção Civil', value: 'Construçao civil' },
  { label: 'Serviços de Utilidade Pública', value: 'Serviços industriais de utilidade pública' },
  { label: 'Transportes e Comunicações', value: 'Transportes e comunicaçoes' },
  { label: 'Administração Pública', value: 'Administraçao pública direta e autárquica' },
  { label: 'Ensino / Educação', value: 'Ensino' },
  { label: 'Saúde (Médicos e Veterinários)', value: 'Serviços médicos, odontológicos e veterinários' },
  { label: 'Alojamento e Alimentação', value: 'Serv. de alojamento, alimentaçao, reparaçao, manutençao, redaçao' },
  { label: 'Agricultura e Pecuária', value: 'Agricultura, silvicultura, criaçao de animais, extrativismo vegetal' },
  { label: 'Indústria Metalúrgica', value: 'Indústria metalúrgica' },
  { label: 'Indústria Mecânica', value: 'Indústria mecânica' },
  { label: 'Indústria de Alimentos/Bebidas', value: 'Indústria de produtos alimentícios, bebidas e álcool etílico' }
];
