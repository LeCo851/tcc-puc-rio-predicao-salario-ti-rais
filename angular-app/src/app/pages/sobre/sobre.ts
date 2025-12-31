import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sobre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sobre.html',
  styleUrl: './sobre.css'
})
export class Sobre {

  tecnologias = [
    { nome: 'Angular 17+', icone: 'bi-filetype-html', desc: 'Frontend moderno e reativo' },
    { nome: 'Spring Boot 4', icone: 'bi-filetype-java', desc: 'Backend robusto em Java' },
    { nome: 'Python & FastAPI', icone: 'bi-filetype-py', desc: 'API de Machine Learning' },
    { nome: 'LightGBM', icone: 'bi-cpu', desc: 'Modelo de Gradient Boosting' },
    { nome: 'Docker', icone: 'bi-box-seam', desc: 'Containerização dos serviços' },
    { nome: 'Highcharts', icone: 'bi-graph-up', desc: 'Visualização de dados interativa' }
  ];

  links = [
    { nome: 'Repositório GitHub', url: 'https://github.com/leandrocoelho/tcc-puc-rio-predicao-salario-ti-rais', icone: 'bi-github' },
    { nome: 'LinkedIn', url: 'https://www.linkedin.com/in/leandro-coelho/', icone: 'bi-linkedin' },
    { nome: 'PUC-Rio', url: 'https://www.puc-rio.br', icone: 'bi-mortarboard-fill' }
  ];

  desafios = [
    {
      titulo: 'Volumetria de Dados (Big Data)',
      problema: 'A base da RAIS possui milhões de registros, tornando o treinamento lento e exigindo muita memória.',
      solucao: 'Utilização de amostragem estratificada (profissionais de TI e relacionados -  cerca de 7 milhões de registros de 2019 a 2024) e otimização de tipos de dados (Parquet) para reduzir o consumo de RAM.'
    },
    {
      titulo: 'Cardinalidade de Variáveis',
      problema: 'Variáveis como "CBO" possuem milhares de categorias, dificultando o uso de One-Hot Encoding.',
      solucao: 'Adoção de Target Encoding (Média Suavizada) para transformar categorias em valores numéricos representativos.'
    },
    {
      titulo: 'Integração de Tecnologias',
      problema: 'Conectar um backend Java com um modelo Python de forma eficiente e escalável.',
      solucao: 'Arquitetura de microsserviços via Docker Compose, com comunicação REST (JSON) entre Spring Boot e FastAPI.'
    },
    {
      titulo: 'Inferência de Senioridade (Proxy & Quartis)',

      problema: 'A base oficial (RAIS) é administrativa e não possui classificação explícita de nível hierárquico (Jr/Pl/Sr/Especialista), o que dificulta a segmentação salarial.',

      solucao: 'Implementou-se uma estratégia composta: validou-se a Idade como variável proxy para experiência e foram aplicados Quartis Dinâmicos sobre ela. Em vez de idades fixas, o algoritmo calcula estatisticamente quem é Júnior (1º Quartil), Pleno (Mediana), Sênior (3º Quartil) e Especialista (9º Decil) especificamente para cada cargo, respeitando as diferentes curvas de maturação de cada carreira.' +
        ' Essa validação é feita em tempo real, toda vez que uma requisição é enviada ao sistema.'
    },

    {
      titulo: 'Robustez Estatística (Fallback)',
      problema: 'Risco de "alucinação estatística" em cenários com baixa volumetria de dados (amostra n < 100).',
      solucao: 'Implementação de Fallback: se a amostra local for insuficiente, o sistema utiliza automaticamente a Média Brasil.'
    },
    {
      titulo: 'Correção Monetária (IPCA)',
      problema: 'Os dados possuem defasagem temporal e valores nominais que não refletem o poder de compra atual.',
      solucao: 'Engenharia financeira no Backend que aplica o IPCA acumulado, corrigindo os valores históricos para o ano atual.'
    }
  ];

}
