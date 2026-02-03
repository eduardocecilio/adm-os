# --- Etapa 1: Build (Construção do Vue) ---
FROM node:18-alpine AS build

WORKDIR /app

# Copia os arquivos de dependência
COPY package*.json ./

# 1. TRUQUE DO MAC vs LINUX:
# Apagamos o package-lock.json gerado no Mac para forçar o Linux 
# a recalcular as dependências para a arquitetura dele.
RUN rm -f package-lock.json

# 2. Instalação Limpa
RUN npm install

# Copia o resto do código
COPY . .

# 3. TRUQUE DA MEMÓRIA:
# Se seu servidor for pequeno (ex: 1GB RAM), o Vite pode estourar a memória.
# Isso garante que ele use o máximo disponível sem crashar.
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Compila para produção
RUN npm run build

# --- Etapa 2: Produção (Servidor Nginx Leve) ---
FROM nginx:alpine

# Copia apenas os arquivos estáticos gerados na etapa anterior
COPY --from=build /app/dist /usr/share/nginx/html

# Expose padrão do Nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]