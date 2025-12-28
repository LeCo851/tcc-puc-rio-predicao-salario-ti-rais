# TCC PUC-Rio - Predição de Salários de TI (RAIS)

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) do MBA em Data Science da PUC-Rio. O objetivo é fornecer uma estimativa salarial para profissionais de Tecnologia da Informação (TI) com base em dados históricos da RAIS (Relação Anual de Informações Sociais), utilizando técnicas de Machine Learning.

## 🏗️ Arquitetura do Projeto

O projeto é composto por dois serviços principais orquestrados via Docker Compose:

1.  **ml-api (Python/FastAPI):**
    *   Responsável por carregar o modelo de Machine Learning treinado (LightGBM).
    *   Recebe os dados do profissional, realiza o pré-processamento (tradução de enums, feature engineering) e executa a inferência.
    *   Expõe um endpoint REST (`/predict`) para consumo.

2.  **spring-app (Java/Spring Boot):**
    *   Atua como backend da aplicação cliente.
    *   Recebe as requisições do frontend (ou cliente API), valida os dados e repassa para a `ml-api`.
    *   Abstrai a comunicação com o serviço de ML.

## 🚀 Tecnologias Utilizadas

*   **Machine Learning & Python:**
    *   Python 3.9+
    *   FastAPI
    *   Pandas, NumPy, Scikit-learn
    *   LightGBM (Modelo de Regressão)
    *   Joblib (Serialização do modelo)

*   **Backend Java:**
    *   Java 17+
    *   Spring Boot 3.x
    *   Maven
    *   Lombok

*   **Infraestrutura:**
    *   Docker & Docker Compose

## 📦 Estrutura de Diretórios

```
tcc-puc-rio-predicao-salario-ti-rais/
├── docker-compose.yml      # Orquestração dos containers
├── ml-api/                 # Serviço de Machine Learning
│   ├── app.py              # Código da API FastAPI
│   ├── Dockerfile          # Definição da imagem Python
│   ├── modelo_salario_ti.pkl # Modelo treinado e artefatos
│   ├── requirements.txt    # Dependências Python
│   └── ...
└── spring-app/             # Aplicação Spring Boot
    ├── src/                # Código fonte Java
    ├── pom.xml             # Dependências Maven
    └── ...
```

## 🛠️ Como Executar

### Pré-requisitos

*   Docker e Docker Compose instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd tcc-puc-rio-predicao-salario-ti-rais
    ```

2.  **Suba os serviços com Docker Compose:**
    Na raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```
    *Isso irá construir as imagens do Python e (futuramente) do Java, e iniciar os containers.*

3.  **Acesse os serviços:**

    *   **API de ML (Documentação Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Spring App:** [http://localhost:8080](http://localhost:8080) (A API estará em `/api/salarios/prever`)

## 🔌 Endpoints Principais

### Spring App (Porta 8080)

*   **POST** `/api/salarios/prever`
    *   Recebe os dados do profissional e retorna a estimativa salarial.
    *   **Exemplo de Payload:**
        ```json
        {
          "cargo": "Analista de desenvolvimento de sistemas",
          "idade": 30,
          "escolaridade": "Superior Completo",
          "tamanho_empresa": "De 50 a 99 funcionários",
          "setor": "Instituições Financeiras (Bancos)",
          "uf": "SP",
          "sexo": "Masculino",
          "raca": "Branca"
        }
        ```

### ML API (Porta 8000)

*   **POST** `/predict`
    *   Endpoint interno utilizado pelo Spring App para realizar a inferência.

## 📊 Modelo de Machine Learning

O modelo utiliza o algoritmo **LightGBM** e foi treinado com dados da RAIS filtrados para ocupações de TI. O processo de inferência envolve:
1.  Tradução de termos em linguagem natural para códigos da RAIS.
2.  Target Encoding para variáveis categóricas de alta cardinalidade (CBO, UF, etc.).
3.  Predição do log do salário e conversão para escala real.

## 📝 Autor

**Leandro Coelho**
MBA em Data Science - PUC-Rio
