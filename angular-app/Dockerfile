# --- Estágio 1: Build ---
FROM node:22.12-alpine AS build
WORKDIR /app

# Copia dependências e instala
COPY package*.json ./
RUN npm install

# Copia o código fonte e gera o build
COPY . .
# Ajuste o comando se seu script de build for diferente
RUN npm run build -- --configuration=production

# --- Estágio 2: Servidor (Nginx) ---
FROM nginx:alpine

# Remove a página padrão do Nginx
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/dist/angular-app/browser /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
