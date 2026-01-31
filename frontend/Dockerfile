# --- Etapa 1: Build (Construção) ---
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Etapa 2: Produção (Nginx) ---
FROM nginx:alpine
# Copia apenas os arquivos estáticos gerados na etapa anterior
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]