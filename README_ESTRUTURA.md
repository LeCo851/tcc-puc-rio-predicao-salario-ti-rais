# TCC PUC-Rio - Predição de Salários de TI (RAIS)

Este projeto é o Trabalho de Conclusão de Curso (TCC) desenvolvido para o **MBA em Data Science & Big Data da PUC-Rio**. O objetivo principal é fornecer uma ferramenta de estimativa salarial para profissionais de Tecnologia da Informação (TI) no Brasil, baseada em dados históricos da RAIS (Relação Anual de Informações Sociais) e utilizando algoritmos avançados de Machine Learning.

## 🏗️ Arquitetura do Sistema

O projeto utiliza uma arquitetura de microsserviços containerizada para garantir escalabilidade e separação de responsabilidades:

1.  **Frontend (angular-app):**
    *   Interface web moderna desenvolvida em **Angular 21+**.
    *   **Estimativa Salarial detalhada:** Formulário dinâmico para consulta de estimativas salariais personalizadas.
    *   **Estimativa Salarial para o Brasil:** Visualização geográfica interativa utilizando **Highmaps**, exibindo médias salariais e volume de profissionais por estado.
    *   **Sobre:** Seção integrada detalhando os desafios técnicos e as soluções estatísticas adotadas.

2.  **spring-app (Backend):**
    *   API REST desenvolvida em Java com Spring Boot 4.
    *  Recebe as requisições do frontend, valida os dados e repassa para o serviço de ML, atua como middleware.
    *   **Correção Monetária:** Aplica o índice IPCA para atualizar valores históricos.
   

3.  **Serviço de ML (ml-api):**
    *   API desenvolvida em **Python** com **FastAPI**.
    *   **Modelo:** Utiliza o modelo **LightGBM** para inferências.
    *   **Processamento:** Realiza Target Encoding dinâmico e tratamento de Big Data utilizando o formato **Parquet**.
    *   **Estatística:** Implementa lógica de **Quartis Dinâmicos** para senioridade usando a **idade** como **variável proxy** e estratégias de **Fallback** para amostras reduzidas.

## 🚀 Tecnologias Utilizadas

*   **Linguagens:** Java 17, Python 3.9+, TypeScript.
*   **Frameworks:** Spring Boot 4, FastAPI, Angular 21.
*   **Ciência de Dados:** Pandas, NumPy, Scikit-learn, LightGBM, Joblib, DuckDB.
*   **Visualização:** Highcharts & Highmaps, Bootstrap 5.
*   **Infraestrutura:** Docker, Docker Compose.
*   **Monitoramento:** Actuator, Prometheus e Grafana.

## 📦 Estrutura do Repositório

```
tcc-puc-rio-predicao-salario-ti-rais/
├── angular-app/            # Frontend Angular
│   ├── src/app/pages/      # Componentes (Home, Dashboard, Sobre)
│   ├── package.json
│   └── ...
├── spring-app/             # Backend Spring Boot
│   ├── src/
│   ├── pom.xml
│   └── ...
├── ml-api/                 # Serviço de Machine Learning
│   ├── app.py
│   ├── Dockerfile
│   ├── modelo_salario_ti.pkl
│   └── ...
└── docker-compose.yml      # Execução containerizada dos 3 serviços
```

## 🛠️ Como Executar

### Pré-requisitos
*   Docker e Docker Compose instalados.
*   Node.js e Java JDK (opcional, apenas para desenvolvimento local fora do Docker).

### Passo a Passo (Docker)
1.  Construa e inicie os serviços:
    ```bash
    docker-compose up --build
    ```
2.  Acesse as aplicações:
    *   **Frontend:** `http://localhost:4200`
    *   **Backend Java:** `http://localhost:8080`
    *   **API Python (Docs):** `http://localhost:8000/docs`
    *   **Grafana:** `http://localhost:3000/`

### Passo a Passo (Produção - Cloud)
1. Acesse a aplicação em produção em `https://tcc-puc-rio-predicao-salario-ti-rais-zc9u.onrender.com/`
2. Back-End java em  `https://tcc-puc-rio-predicao-salario-ti-rais-1.onrender.com/actuator/health`
3. FastAPI em `https://tcc-puc-rio-predicao-salario-ti-rais.onrender.com/docs`

## 📝 Metodologia e Diferenciais

*   **Variável Proxy:** Uso da idade como substituto estatístico para tempo de experiência.
*   **Senioridade Dinâmica:** Classificação (Jr/Pl/Sr/Esp) baseada na distribuição real de cada cargo (Quartis), feito em tempo real pelo sistema, evitando cortes arbitrários.
*   **Robustez:** Sistema de Fallback automático para médias nacionais quando a amostra regional é insuficiente ($n < 100$).
*   **Atualização Monetária:** Todos os resultados são corrigidos pela inflação acumulada (IPCA).

## 👤 Autor

**Leandro Coelho**
Engenheiro de software e Cientista de Dados.
