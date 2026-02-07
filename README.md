# 📊 AdmOS - Inteligência Corporativa (Core)

> **Ambiente de Produção e Desenvolvimento Full Stack**

Este é o repositório principal do **AdmOS**, uma plataforma de BI focada em gestão financeira, contábil e análise de ativos. A arquitetura foi desenhada para ser modular, facilitando a inclusão de novos modelos de cálculo e integrações de API.

---

## 🛠️ Arquitetura e Higiene do Projeto

O sistema é dividido em camadas independentes para garantir a escalabilidade:

### 1. Backend (FastAPI + Pandas)

* **Processamento:** Engine central em Python utilizando `Pandas` para cálculos matriciais e `NumPy` para lógica financeira.
* **Segurança:** Implementação de dependência global `x-token` via `APIKeyHeader`.
* **Ambiente:** Variáveis sensíveis gerenciadas via `.env` (não versionado).
* **Integrações:** Consumo assíncrono de APIs financeiras (Yahoo Finance, BrasilAPI).

### 2. Frontend (Vue.js 3 + Vite)

* **Componentização:** Interface modular baseada em `ModuleLayout`.
* **Roteamento:** Vue Router configurado para modo History (Nginx fallback).
* **Visualização:** Renderização dinâmica de gráficos SVG e Sparklines para performance.

### 3. Infraestrutura (DevOps)

* **Docker:** Containerização completa (Backend/Frontend).
* **Nginx:** Atua como servidor de arquivos estáticos e proxy reverso para a SPA.
* **Deploy:** Fluxo GitOps automatizado via Portainer (Mini-150).

---

## 🚀 Configuração do Ambiente

### Variáveis de Ambiente (`.env`)

Certifique-se de configurar os arquivos `.env` na raiz das pastas correspondentes:

**Backend:**

```env
API_TOKEN=seu_token_aqui
ENV=development # ou production

```

**Frontend:**

```env
VITE_API_URL=http://localhost:8001
VITE_API_TOKEN=seu_token_aqui

```

---

## 📦 Gestão de Dependências

### Backend

Sempre que adicionar uma biblioteca, atualize o manifesto:

```bash
pip freeze > requirements.txt

```

*(As dependências críticas incluem `openpyxl` para exportação e `slowapi` para segurança).*

### Frontend

```bash
npm install

```

---

## 🚢 Deploy e Produção

O deploy é acionado via push na branch `main`. No **Portainer**:

1. Acesse a Stack `adm-os`.
2. Clique em **Update the stack**.
3. Ative a opção **"Re-pull image"** para reconstruir os containers com as novas dependências e configurações de Nginx.

---

## 📄 Notas de Manutenção

* **CORS:** Em produção, as origens são restritas ao domínio oficial.
* **Logs:** Verifique os logs do container backend para monitorar tentativas de acesso não autorizado (401).

**Desenvolvido por Eduardo Cecílio** 🚀

---