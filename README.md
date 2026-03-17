# AdmOS - Inteligência Corporativa

> Plataforma de BI focada em gestão financeira, contábil e análise de ativos.

---

## Quick Start (Docker)

```bash
cp .env.example .env
# edite o .env com seus valores
docker compose up --build
```

Acesse: [http://localhost:8082](http://localhost:8082)

---

## Configuração

### 1. Variáveis de Ambiente

Copie o arquivo de exemplo e preencha com seus valores:

```bash
cp .env.example .env
```

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Chave JWT — gere com `python -c "import secrets; print(secrets.token_hex(32))"` |
| `RESET_SECRET_KEY` | Chave JWT para reset de senha — gere da mesma forma |
| `DATABASE_URL` | URL completa do PostgreSQL |
| `POSTGRES_USER` | Usuário do banco |
| `POSTGRES_PASSWORD` | Senha do banco |
| `POSTGRES_DB` | Nome do banco |
| `FRONTEND_URL` | URL pública do frontend (usada em links de e-mail e CORS) |
| `N8N_WEBHOOK_URL` | Endpoint do n8n para envio de e-mails |
| `N8N_WEBHOOK_TOKEN` | Token de autenticação do webhook n8n |
| `EMAIL_FROM` | Remetente dos e-mails (ex: `Sistema <nao-responda@seudominio.com>`) |
| `VITE_API_URL` | Prefixo da API no frontend (padrão: `/api`) |

### 2. Subir os containers

```bash
docker compose up -d
```

---

## Arquitetura

```
[Cloudflare Tunnel / Nginx] → [frontend:80] → [backend:8000] → [db:5432]
```

- **Backend** (FastAPI + Python): API REST, autenticação JWT, cálculos financeiros
- **Frontend** (Vue.js 3 + Vite + Nginx): SPA com proxy reverso para `/api`
- **Banco** (PostgreSQL 15): dados isolados em rede interna Docker
- **Rede**: `frontend` exposto na `infra_net` para acesso via Cloudflare Tunnel; `backend` e `db` apenas na rede interna

---

## Testes

```bash
docker compose exec backend python -m pytest
```

---

## Deploy com Portainer

1. Crie uma Stack com o conteúdo do `docker-compose.yml`
2. Configure as variáveis de ambiente na aba **Environment variables**
3. Para atualizar: **Update the stack** → marque **Re-pull image**

---

**Desenvolvido por Eduardo Cecílio**
