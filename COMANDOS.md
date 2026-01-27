Tem toda razão, Eduardo. Peço desculpas. O erro foi meu na hora de fechar as crases (`````) no bloco de código anterior, o que fez o Markdown "engolir" o texto explicativo como se fosse código.

Aqui estão os dois arquivos corrigidos, separados e formatados corretamente para você apenas copiar e colar.

### 1. Arquivo `COMANDOS.md` (Corrigido)

Abra o arquivo `COMANDOS.md`, apague tudo e cole exatamente o conteúdo abaixo:

```markdown
# ⚡ Guia Rápido de Comandos - AdminOS

Este arquivo contém os comandos essenciais para rodar o projeto no dia a dia.

## 1. Backend (Python/FastAPI)
O "cérebro" do sistema. Precisa estar rodando para os cálculos funcionarem.

**Passo 1: Entrar na pasta e ativar o ambiente virtual**
```bash
cd backend
source venv/bin/activate

```

**Passo 2: Ligar o Servidor**

```bash
uvicorn main:app --reload

```

* O servidor ficará rodando em: `http://127.0.0.1:8000`
* Documentação automática: `http://127.0.0.1:8000/docs`

---

## 2. Frontend (Vue.js)

A "cara" do sistema.

**Passo 1: Entrar na pasta**

```bash
cd frontend

```

**Passo 2: Ligar o Site**

```bash
npm run dev

```

* O site abrirá em: `http://localhost:5173`

---

## 3. Git (Manutenção)

Como salvar seu trabalho na nuvem.

**Salvar tudo e enviar:**

```bash
git add .
git commit -m "Escreva aqui o que você fez"
git push

```

**Baixar atualizações (se mexeu de outro PC):**

```bash
git pull

```