# 🚀 Guia de Implantação (AdmOS) - Ubuntu Server

Este guia descreve como implantar o projeto **AdmOS** (versão com Autenticação e PostgreSQL) em um servidor Ubuntu usando Docker.

## ✅ Pré-requisitos
-   Servidor Ubuntu (20.04 ou 22.04 LTS).
-   Acesso SSH.
-   Git instalado.
-   Docker e Docker Compose instalados.

### 1. Instalar Docker e Docker Compose
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# (Faça logout e login novamente para aplicar permissões de grupo)
```

## 📦 Implantação

### 1. Clonar o Repositório
```bash
git clone https://github.com/seusrouser/adm-os.git
cd adm-os
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` baseado no exemplo (se houver) ou configure manualmente:
```bash
# Backend .env (backend/.env) ou raiz se configurado pelo docker-compose
# Neste projeto, o docker-compose repassa variáveis ou você pode criar um .env na raiz (recomendado)

cat <<EOF > .env
API_TOKEN=sua_chave_secreta_super_segura_para_jwt
POSTGRES_USER=admos
POSTGRES_PASSWORD=admos_password_segura
POSTGRES_DB=admos_db
EOF
```
*Certifique-se que o `docker-compose.yml` está lendo essas variáveis ou ajuste o arquivo conforme necessário.*

### 3. Subir os Containers
### Executando com imagens prontas do GitHub (Padrão/Mais Rápido)
No dia a dia, após um `git push` na branch main, as imagens serão construídas pelo GitHub Actions e postadas no GHCR.

Para atualizar o servidor:
```bash
git pull origin main
docker compose pull
docker compose up -d
```

### Emergência / Build Local (Fallback)
Se não estiver usando o CI/CD ou a Action falhar, você pode forçar a compilação local (que usará os Dockerfiles do `./backend` e `./frontend`):

```bash
git pull origin main
docker compose up -d --build
```
Isso iniciará:
-   `adm-os-db` (PostgreSQL)
-   `adm-os-backend` (FastAPI)
-   `adm-os-frontend` (Vue.js + Nginx)

### 4. Executar Migrações do Banco de Dados
Para criar as tabelas iniciais (Users, History, etc), execute o Alembic dentro do container backend:
```bash
docker-compose exec backend alembic upgrade head
```

### 5. Verificar Status
```bash
docker-compose ps
```
Todos os serviços devem estar "Up".

### 6. Acessar
Abra seu navegador e acesse o IP do servidor:
`http://SEU_IP_DO_SERVIDOR:8082`

Você verá a tela de Login.

## 🔄 Atualização (Deploy Contínuo Manual)
Para atualizar o código no futuro:
```bash
git pull origin main
docker-compose up -d --build
docker-compose exec backend alembic upgrade head
```
