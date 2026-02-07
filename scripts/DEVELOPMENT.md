# 🛠️ Guia de Desenvolvimento - AdmOS

Este guia centraliza as instruções para manter o ambiente de desenvolvimento consistente entre sistemas (Windows/macOS) e garantir a integridade da stack.

---

## ⚙️ Configuração do Ambiente

### 1. Requisitos de Sistema

* **Node.js**: v18+ (LTS recomendado)
* **Python**: v3.12 (Recomendado para evitar conflitos de bibliotecas como Pandas/Numpy)

### 2. Backend (FastAPI)

O backend gerencia a lógica de negócio e integrações financeiras.

**Setup Inicial:**

```powershell
# Windows
cd backend
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# macOS / Linux
cd backend
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

```

### 3. Frontend (Vue.js)

```bash
cd frontend
npm install

```

---

## 🚀 Fluxo de Trabalho Diário

### Execução Local

Para rodar o projeto, utilize o servidor de desenvolvimento do Vite e o modo reload do Uvicorn:

* **Backend:** `uvicorn main:app --reload --port 8001`
* **Frontend:** `npm run dev`

### Higiene de Dependências

Sempre que instalar um novo pacote no Python (ex: `slowapi` ou `openpyxl`), atualize o manifesto imediatamente para que o **Portainer** possa refletir as mudanças no servidor:

```bash
pip freeze > requirements.txt

```

---

## ⚠️ Troubleshooting (Solução de Problemas)

### Erros de Compilação (Windows)

Se encontrar erros de `subprocess-exited-with-error` ao instalar **Pandas** ou **Numpy**:

1. Certifique-se de que não está usando Python experimental (v3.13 ou v3.14).
2. Remova as versões fixas do `requirements.txt` para que o `pip` busque os arquivos pré-compilados (Wheels).

### Erro de PATH / SSL (Windows)

Evite pastas com acentos (ex: `Computação`). O Python e o `curl_cffi` podem falhar ao localizar certificados SSL em caminhos com caracteres especiais.

* **Recomendação:** `C:\Projetos\adm-os`

### Erro de Execução de Scripts (PowerShell)

Se não conseguir ativar a `venv`:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 🔒 Segurança em Desenvolvimento

* **Variáveis de Ambiente:** Nunca remova a entrada `.env` do arquivo `.gitignore`.
* **CORS:** O arquivo `main.py` está configurado para aceitar `localhost` e o domínio oficial. Caso mude a porta do Vite, atualize a lista de `origins`.

---