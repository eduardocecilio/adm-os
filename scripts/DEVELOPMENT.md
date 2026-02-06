# 🛠️ Guia de Desenvolvimento - AdmOS

Este documento contém todas as instruções técnicas para configurar o ambiente, rodar o projeto e entender a estrutura de pastas, tanto para Windows quanto para macOS/Linux.

---

## ⚙️ Configuração Inicial (Primeira vez)

Antes de rodar, você precisa instalar as dependências.

### 1. Pré-requisitos

* **Node.js** (v18 ou superior)
* **Python** (v3.10 ou superior)

### 2. Configurando o Backend (Python)

**Windows (PowerShell):**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

```

**Mac / Linux:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 3. Configurando o Frontend (Node.js)

**Qualquer Sistema:**

```bash
cd frontend
npm install

```

---

## 🚀 Como Rodar o Projeto (Dia a Dia)

Existem duas formas de rodar: usando os scripts automáticos (recomendado) ou manualmente.

### Opção A: Modo Automático (Recomendado)

Estes scripts abrem o Backend e o Frontend simultaneamente.

* **No Windows:** Dê dois cliques no arquivo `run.bat` na raiz ou digite no terminal:
```powershell
.\run.bat

```


* **No Mac / Linux:** No terminal, digite:
```bash
./run.sh

```



### Opção B: Modo Manual

Se precisar rodar separadamente para ver logs de erro específicos:

**Terminal 1 (Backend):**

```bash
cd backend
# Windows:
.\venv\Scripts\activate
# Mac:
source venv/bin/activate

uvicorn main:app --reload

```

**Terminal 2 (Frontend):**

```bash
cd frontend
npm run dev

```

---

## 📦 Banco de Dados (SQLite)

O projeto utiliza **SQLite** para desenvolvimento local.

* O arquivo do banco (`adm_os.db`) é criado automaticamente na pasta `backend/` ao rodar o projeto pela primeira vez.
* **Atenção:** Este arquivo está no `.gitignore`. Se você mudar de computador, terá um banco vazio no novo local.

---

## ⚠️ Solução de Problemas Comuns

### Erro de Certificado SSL (Windows)

Se o Yahoo Finance der erro `curl 77`, verifique se o caminho da pasta do projeto contém acentos ou espaços (ex: `Computação`).
**Solução:** Mova o projeto para um caminho simples, ex: `C:\Projetos\adm-os`.

### Erro "Script não pode ser carregado" (Windows)

Se ao ativar a venv der erro de permissão.
**Solução:** Rode no PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Erro "Vite não reconhecido"

Isso ocorre se você clonou o projeto mas não instalou as dependências do front.
**Solução:** Entre na pasta `frontend` e rode `npm install`.

```

---

### O que melhoramos aqui?

1.  **Profissionalismo:** Mudamos de "uma lista de comandos" para um "Guia de Desenvolvimento".
2.  **Cross-Platform:** Agora serve tanto para o seu Mac quanto para o Windows que você está usando agora.
3.  **Troubleshooting:** Adicionei a seção de "Solução de Problemas" com o erro do acento ("Computação") e do SSL que acabamos de resolver. Isso é **ouro** para documentação. Se você esquecer daqui a 3 meses, está escrito lá.

Pode criar esse arquivo, dar o commit e o push! 🚀

```