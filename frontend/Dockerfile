# --- Etapa 1: Build (Construção do Vue) ---
# Atualizado para Node 20 para suportar Vite v7+
FROM node:20-alpine AS build

WORKDIR /app

# Copia arquivos de dependência
COPY package*.json ./

# Limpeza de segurança para evitar conflitos Mac vs Linux
RUN rm -f package-lock.json

# Instalação completa das dependências
RUN npm install

# Copia o resto do código
COPY . .

# Compila para produção
RUN npm run build

# --- Etapa 2: Produção (Servidor Nginx Leve) ---
FROM nginx:alpine

# Copia os arquivos estáticos gerados
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]