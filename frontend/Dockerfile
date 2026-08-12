# --- Etapa 1: Build ---
FROM node:20.19.5-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Etapa 2: Producao ---
# Nginx unprivileged: roda como uid 101 e escuta em 8080 (nao 80)
FROM nginxinc/nginx-unprivileged:1.30.4-alpine-slim
USER root
RUN apk upgrade --no-cache
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
USER nginx
CMD ["nginx", "-g", "daemon off;"]
