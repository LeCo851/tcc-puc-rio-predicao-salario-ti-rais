# TCC PUC-Rio - Predição de Salários de TI (RAIS)

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) do MBA em Data Science da PUC-Rio. O objetivo é fornecer uma estimativa salarial para profissionais de Tecnologia da Informação (TI) com base em dados históricos da RAIS (Relação Anual de Informações Sociais), utilizando técnicas de Machine Learning.

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura de microsserviços composta por três camadas principais:

1.  **angular-app (Frontend):**
    *   Interface web desenvolvida em Angular.
    *   Permite ao usuário inserir seus dados (cargo, escolaridade, etc.) de forma amigável.
    *   Consome a API do backend (`spring-app`).

2.  **spring-app (Backend):**
    *   API REST desenvolvida em Java com Spring Boot.
    *   Atua como middleware e gateway.
    *   Recebe as requisições do frontend, valida os dados e repassa para o serviço de ML.

3.  **ml-api (Machine Learning Service):**
    *   Serviço Python/FastAPI.
    *   Carrega o modelo LightGBM treinado.
    *   Realiza o pré-processamento e a inferência salarial.

## 🚀 Tecnologias Utilizadas

*   **Frontend Web:**
    *   Angular 17+
    *   TypeScript
    *   HTML5 / CSS3
    *   Node.js & NPM

*   **Backend Java:**
    *   Java 17+
    *   Spring Boot 3.x
    *   Maven
    *   Lombok

*   **Machine Learning & Python:**
    *   Python 3.9+
    *   FastAPI
    *   Pandas, NumPy, Scikit-learn
    *   LightGBM (Modelo de Regressão)
    *   Joblib

*   **Infraestrutura:**
    *   Docker & Docker Compose

## 📦 Estrutura de Diretórios

```
tcc-puc-rio-predicao-salario-ti-rais/
├── angular-app/            # Frontend Angular
│   ├── src/
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
└── docker-compose.yml      # Orquestração (ML API)
```

## 🛠️ Como Executar

### Pré-requisitos

*   Docker e Docker Compose.
*   Java JDK 17+ e Maven (para rodar o backend localmente).
*   Node.js e NPM (para rodar o frontend localmente).

### Passo a Passo

#### 1. Serviço de Machine Learning (Docker)
O serviço de ML está containerizado. Na raiz do projeto, execute:
```bash
docker-compose up --build
```
*   O serviço estará disponível em: `http://localhost:8000`

#### 2. Backend (Spring Boot)
Em um novo terminal, navegue até a pasta `spring-app` e execute:
```bash
cd spring-app
./mvnw spring-boot:run
```
*   A API estará disponível em: `http://localhost:8080`

#### 3. Frontend (Angular)
Em outro terminal, navegue até a pasta `angular-app`, instale as dependências e inicie o servidor:
```bash
cd angular-app
npm install
ng serve
```
*   Acesse a aplicação no navegador em: `http://localhost:4200`

## 🔌 Endpoints e Fluxo

1.  **Usuário** acessa `http://localhost:4200` e preenche o formulário.
2.  **Angular** envia POST para `http://localhost:8080/api/salarios/prever`.
3.  **Spring Boot** repassa a requisição para `http://localhost:8000/predict`.
4.  **ML API** retorna o salário estimado, que faz o caminho inverso até o usuário.

## 📝 Autor

**Leandro Coelho**
MBA em Data Science - PUC-Rio
