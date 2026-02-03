# --- Etapa 1: Build ---
FROM node:18-alpine AS build

# Instala dependências necessárias para compilação no Alpine
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Garante permissões na pasta
RUN chown -R node:node /app
USER node

COPY --chown=node:node package*.json ./

# Instala TUDO (incluindo devDependencies como o Vite)
RUN npm install

COPY --chown=node:node . .

# Comando de build com log detalhado para debug
RUN npm run build

# --- Etapa 2: Produção ---
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]