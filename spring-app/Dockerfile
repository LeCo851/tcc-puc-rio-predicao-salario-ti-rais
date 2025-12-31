# --- ESTÁGIO 1: BUILD (Compilação) ---
# Usa uma imagem oficial do Maven com Java 17 para compilar o projeto
FROM maven:3.9.6-eclipse-temurin-17 AS build

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro (para aproveitar cache do Docker)
COPY pom.xml .

# Baixa as dependências (sem copiar o código fonte ainda, para ser mais rápido nas próximas vezes)
RUN mvn dependency:go-offline

# Agora sim, copia o código fonte do projeto
COPY src ./src

# Compila o projeto e gera o arquivo .jar (pula os testes para ser mais rápido no deploy)
RUN mvn clean package -DskipTests

# --- ESTÁGIO 2: RUNTIME (Execução) ---
# Usa uma imagem Java bem leve (Alpine Linux) só para rodar o app
FROM eclipse-temurin:17-jre-alpine

# Cria o diretório da aplicação
WORKDIR /app

# Copia apenas o arquivo .jar gerado no estágio anterior
# O nome 'app.jar' padroniza a execução
COPY --from=build /app/target/*.jar app.jar

# Informa ao Render que a aplicação roda na porta 8080
EXPOSE 8080

# Comando que faz o Java rodar o seu programa
ENTRYPOINT ["java", "-jar", "app.jar"]