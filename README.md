# AdmOS — inteligência corporativa

O AdmOS é uma plataforma web de inteligência corporativa para organizar
informações financeiras, contábeis, estratégicas e de investimentos. O projeto
reúne uma API FastAPI, uma SPA Vue e PostgreSQL em uma arquitetura full stack.

## Funcionalidades

- organizações, membros e papéis de acesso por workspace;
- autenticação, recuperação de senha e convites por e-mail;
- balanço patrimonial, DRE, indicadores e comparação de períodos;
- análises de NPS e de operações de swing trade;
- exportação de relatórios em XLSX;
- ambiente reproduzível com Docker Compose, migrations e CI.

## Quick Start local com Docker

Pré-requisito: Docker com o comando `docker compose` disponível.

```bash
cp .env.example .env
openssl rand -hex 32
openssl rand -hex 32
openssl rand -hex 32
```

Cole os três valores gerados, respectivamente, em `SECRET_KEY`,
`RESET_SECRET_KEY` e `POSTGRES_PASSWORD` no `.env`. Eles devem ser diferentes.
Os campos vazios de integração com e-mail podem continuar vazios.

Valide e inicie a aplicação:

```bash
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

- Frontend: <http://localhost:8082>
- Backend local: <http://localhost:8000>
- Documentação da API local: <http://localhost:8000/docs>

O Compose constrói as imagens a partir do código, cria a rede e o volume local,
aguarda o PostgreSQL e aplica as migrations antes de iniciar a API. Nenhuma
imagem privada, rede Docker externa ou volume previamente criado é necessário.
As portas publicadas ficam restritas ao loopback (`127.0.0.1`).

Para acompanhar ou encerrar:

```bash
docker compose logs -f
docker compose down
```

Para também apagar o banco local da aplicação:

```bash
docker compose down --volumes
```

## Configuração

O arquivo `.env.example` contém apenas valores locais não secretos e campos
secretos vazios. O Compose falha antes de iniciar caso qualquer segredo
obrigatório continue vazio.

| Variável | Obrigatória | Uso |
| --- | --- | --- |
| `SECRET_KEY` | sim | Assinatura dos tokens de acesso; gere um valor exclusivo |
| `RESET_SECRET_KEY` | sim | Assinatura dos tokens de redefinição; use outro valor exclusivo |
| `POSTGRES_PASSWORD` | sim | Senha local do PostgreSQL; gere um terceiro valor exclusivo |
| `POSTGRES_USER` | não | Usuário local do banco, padrão `adm_os` |
| `POSTGRES_DB` | não | Banco local, padrão `adm_os` |
| `APP_PORT` | não | Porta loopback do frontend, padrão `8082` |
| `BACKEND_PORT` | não | Porta loopback da API, padrão `8000` |
| `FRONTEND_URL` | não | Origem usada em CORS e links de e-mail |
| `ALLOW_PUBLIC_REGISTRATION` | não | Mantém cadastro sem convite bloqueado fora de localhost; padrão `false` |
| `VITE_API_URL` | não | Prefixo público da API no JavaScript, padrão `/api` |
| `N8N_WEBHOOK_URL` | não | Endpoint opcional para envio de e-mail |
| `N8N_WEBHOOK_TOKEN` | não | Credencial opcional do webhook; nunca versione |
| `EMAIL_FROM` | não | Remetente usado pela integração opcional; obrigatório quando o webhook estiver ativo |

Variáveis `VITE_*` são incorporadas ao bundle entregue ao navegador. Elas
nunca devem conter tokens, senhas ou qualquer outro segredo.

Com `ALLOW_PUBLIC_REGISTRATION=false`, a criação da primeira conta continua
funcionando no Quick Start em `localhost`, mas uma instalação acessada por host
externo exige convite. Não altere esse controle sem implementar proteção contra
abuso e revisar novamente o fluxo de cadastro.

## Arquitetura local

```text
navegador -> 127.0.0.1:8082 -> frontend (Nginx)
                                  | /api
                                  v
                              backend -> PostgreSQL
```

- **Backend:** FastAPI, SQLAlchemy, autenticação JWT e cálculos financeiros.
- **Frontend:** Vue 3, Vite e Nginx com proxy de `/api`.
- **Banco:** PostgreSQL 15 em volume e rede gerenciados pelo Compose, sem porta
  publicada no host.

Os cálculos e indicadores devem ser validados conforme o contexto de uso e não
constituem aconselhamento financeiro, contábil, fiscal ou de investimento.

## Verificação

O workflow de CI possui somente permissão `contents: read`, não recebe segredos
do repositório e não publica imagens ou artefatos. Ele valida o Compose, constrói
as duas imagens localmente e executa os testes do backend com SQLite efêmero.

Localmente, depois de preencher o `.env`:

```bash
docker compose build
docker compose run --rm --no-deps \
  -e DATABASE_URL=sqlite:////tmp/adm-os-test.db \
  backend python -m pytest
```

## Segurança, operação e direitos

Leia [SECURITY.md](SECURITY.md) antes de executar ou estudar o projeto. O guia
[DEPLOY.md](DEPLOY.md) documenta a execução local e os requisitos para uma
eventual implantação externa.

Este repositório não inclui uma licença de software. Tornar o código visível não
concede automaticamente permissão para copiar, modificar ou redistribuir; veja
[NOTICE](NOTICE).

**Autor:** Eduardo Cecílio
