# Guia de Deploy - AdmOS

Deploy em servidor Ubuntu com Docker.

---

## Pré-requisitos

- Ubuntu 20.04 / 22.04 LTS
- Docker e Docker Compose instalados

```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# logout/login para aplicar o grupo
```

---

## Deploy

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/adm-os.git
cd adm-os
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` e preencha todos os valores. Veja a tabela no README para descrição de cada variável.

Gere as chaves JWT:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Subir os containers

```bash
docker compose up -d
```

Verifique se estão rodando:
```bash
docker compose ps
```

### 4. Migrations do banco

Na primeira vez:
```bash
docker compose exec backend alembic upgrade head
```

---

## Cloudflare Tunnel (opcional)

Se usar Cloudflare Tunnel, o frontend está na rede `infra_net`. Configure a regra no dashboard:

```
seu-dominio.com → http://adm-os-frontend:80
```

---

## Atualização

```bash
git pull origin main
docker compose pull
docker compose up -d
docker compose exec backend alembic upgrade head
```

---

## Build local (sem CI/CD)

```bash
git pull origin main
docker compose up -d --build
docker compose exec backend alembic upgrade head
```
