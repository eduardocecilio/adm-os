# --- Etapa 1: Build (Construção do Vue) ---
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
# O ajuste que sugeri antes:
RUN npm install --include=dev
COPY . .
RUN npm run build

# --- Etapa 2: Produção (Servidor Nginx Leve) ---
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]