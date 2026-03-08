# 📊 AdmOS - Inteligência Corporativa (Core)

> **Ambiente de Produção e Desenvolvimento Full Stack**

Este é o repositório principal do **AdmOS**, uma plataforma de BI focada em gestão financeira, contábil e análise de ativos. A arquitetura foi desenhada para ser modular, facilitando a inclusão de novos modelos de cálculo e integrações de API.

---

## 🚀 Quick Start (Docker)

A maneira mais fácil e recomendada de rodar o projeto é via Docker. Isso garante que todas as dependências (Python, Node.js, Banco de Dados) estejam isoladas e configuradas corretamente.

```bash
# Na raiz do projeto
docker-compose up --build
```
- **Frontend:** [http://localhost:8082](http://localhost:8082) (ou `https://adm.ceciliolab.com` em produção)
- **Backend:** Acessível internamente via container ou `/api` (não exposto diretamente).

---

## 🛠️ Arquitetura

O sistema é dividido em camadas independentes para garantir a escalabilidade:

### 1. Backend (FastAPI + Pandas)
*   **Processamento:** Engine central em Python utilizando `Pandas` para cálculos matriciais e `NumPy` para lógica financeira.
*   **Segurança:** Implementação de dependência global `x-token` via `APIKeyHeader`.
*   **Ambiente:** Variáveis sensíveis gerenciadas via `backend/.env`.
*   **Testes:** Suíte automatizada com `pytest`.

### 2. Frontend (Vue.js 3 + Vite)
*   **Componentização:** Interface modular baseada em `ModuleLayout`.
*   **API:** Serviço centralizado (`api.js`) com fallback inteligente para desenvolvimento e produção.
*   **Visualização:** Renderização dinâmica de gráficos SVG e Sparklines.

### 3. Infraestrutura (DevOps)
*   **Docker:** Containerização completa.
*   **Nginx:** Atua como servidor de arquivos estáticos e proxy reverso para a API, eliminando a necessidade de CORS complexo em produção.

---

## ⚙️ Configuração do Ambiente

### Variáveis de Ambiente (`.env`)

Certifique-se de criar os arquivos `.env` na raiz das pastas correspondentes:

**Backend (`backend/.env`):**
```env
API_TOKEN=seu_token_secreto
DATABASE_URL=sqlite:///./adm_os.db
```

**Frontend (`frontend/.env.development`):**
```env
VITE_API_URL=/api
VITE_API_TOKEN=seu_token_secreto
```

---

## 📦 Gestão de Dependências

### Backend (Python)
Sempre que adicionar uma biblioteca, atualize o manifesto para garantir que o container Docker instale tudo corretamente:

```bash
# Dentro da pasta backend
pip freeze > requirements.txt
```

### Frontend (Node.js)
```bash
# Dentro da pasta frontend
npm install
```

---

## 🧪 Testes Automatizados

Para rodar os testes do backend dentro do container (garantindo o mesmo ambiente de produção):

```bash
docker-compose exec backend python -m pytest
```

---

## 🚢 Deploy e Produção

O deploy é acionado via push na branch `main`. No **Portainer**:

1.  Acesse a Stack `adm-os`.
2.  Clique em **Update the stack**.
3.  Ative a opção **"Re-pull image"** para reconstruir os containers.

---

**Desenvolvido por Eduardo Cecílio** 🚀