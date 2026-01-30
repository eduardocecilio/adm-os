# 📊 AdminOS - Inteligência Corporativa

> **Projeto Full Stack** unindo Administração Estratégica e Engenharia de Software.

O **AdminOS** é uma plataforma de Business Intelligence (BI) projetada para centralizar a gestão financeira e contábil. O sistema oferece ferramentas avançadas para análise de balanços, DRE, indicadores de performance e monitoramento de mercado financeiro em tempo real.

![Status do Projeto](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Vue.js](https://img.shields.io/badge/Frontend-Vue.js_3-4FC08D)
![Python](https://img.shields.io/badge/Backend-Python_FastAPI-3776AB)

---

## 🖥️ Preview Visual

*(Adicione aqui um print da tela de Dashboard de Investimentos ou dos Indicadores Contábeis)*

---

## 🚀 Funcionalidades Principais

### 1. 💰 Módulo de Contabilidade (Novo)
Ferramenta completa para análise vertical e horizontal das demonstrações financeiras.
- **Entrada de Dados:** Interface para lançamento de **Balanço Patrimonial** e **DRE**.
- **Cálculo Automático de KPIs:**
  - **Liquidez:** Corrente, Seca, Imediata e Geral.
  - **Rentabilidade:** ROI, ROE, ROA e Margem Líquida.
  - **Atividade:** Prazos Médios (PME, PMR, PMP) e Ciclos Operacional/Financeiro.
  - **Estrutura de Capital:** Grau de Endividamento.
- **Evolução Patrimonial:** Gráficos interativos comparando a evolução do Ativo, Passivo e PL ao longo do tempo.
- **Histórico:** Salvamento de versões e comparação entre períodos.
- **Exportação:** Relatórios detalhados em **Excel (.xlsx)**.

### 2. 📈 Módulo de Investimentos (Market Data)
Monitoramento em tempo real conectado a APIs financeiras globais.
- **Integração Yahoo Finance & BrasilAPI:** Dados reais sem delay.
- **Câmbio & Cripto:** Cotação de Dólar, Euro e Bitcoin (com conversão automática BRL/USD).
- **Indicadores Macro:** Acompanhamento da **Taxa Selic** e **IPCA** (Inflação).
- **Gráficos Dinâmicos:** Sparklines (mini-gráficos) gerados via SVG com variação histórica (1D, 1M, 1A).

### 3. ⚖️ Cálculos de Swing Trade
- Apuração de lucro líquido.
- Cálculo automático de DARF (Imposto de Renda) com alíquotas de 15% ou 20%.

---

## 🛠 Tecnologias e Arquitetura

### Frontend (Client)
- **Vue.js 3 (Composition API):** Reatividade e gestão de estado.
- **Vite:** Build tool de alta performance.
- **CSS3 Scoped:** Design responsivo e componentes modulares (Cards, Modais, Gráficos SVG).

### Backend (Server)
- **Python 3.9+:** Núcleo de processamento de dados.
- **FastAPI:** API RESTful assíncrona e veloz.
- **Pandas & NumPy:** Motor matemático para cálculos financeiros complexos e manipulação de DataFrames.
- **YFinance & Requests:** Web Scraping e consumo de APIs externas.

---

## 📦 Como Rodar o Projeto

### Pré-requisitos
* Node.js (v16+)
* Python (v3.9+)

### Passo a Passo Rápido

1. **Clone o repositório:**
```bash
git clone [https://github.com/seu-usuario/admin-os.git](https://github.com/seu-usuario/admin-os.git)
cd admin-os

```

2. **Backend (API):**
```bash
cd backend
python -m venv venv
# Ative o venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload

```


3. **Frontend (Interface):**
```bash
cd frontend
npm install
npm run dev

```


4. **Acesse:** Abra `http://localhost:5173` no navegador.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

**Desenvolvido por Eduardo Cecílio** 🚀

```

### O que eu melhorei:

1.  **Destaquei a Contabilidade e o Mercado:** Eram as partes mais complexas que fizemos hoje (Gráficos SVG, Pandas, Yahoo Finance), elas precisavam estar em primeiro lugar.
2.  **Tecnologias:** Adicionei `Pandas` e `YFinance`, pois são diferenciais técnicos importantes do seu backend.
3.  **Badges:** Coloquei aquelas "medalhas" coloridas no topo. Isso dá um ar muito profissional em repositórios do GitHub.
4.  **Status:** Deixei claro que está "Em Desenvolvimento".

### 💡 Dica de Ouro para seu Portfólio:
**Tire um Print da tela!**
No lugar onde escrevi `*(Adicione aqui um print...)*`, tire um screenshot bonito da tela com os gráficos de evolução que acabamos de fazer e coloque a imagem na pasta do projeto (ex: `assets/preview.png`). Isso aumenta drasticamente o interesse de quem visita seu GitHub.

```