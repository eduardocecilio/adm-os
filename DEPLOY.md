# Execução e implantação do AdmOS

## Escopo

O Compose versionado configura uma **execução local em loopback**. Uma
implantação em servidor, Portainer, Cloudflare Tunnel, Kubernetes ou qualquer
exposição pública exige os controles adicionais descritos neste documento.

## Execução local

Pré-requisitos:

- Git;
- Docker Engine ou Docker Desktop;
- Docker Compose v2 (`docker compose`);
- OpenSSL para gerar valores aleatórios.

```bash
git clone <URL_DO_REPOSITORIO>
cd adm-os
cp .env.example .env
openssl rand -hex 32
openssl rand -hex 32
openssl rand -hex 32
```

Edite o `.env` e cole os três resultados diferentes em `SECRET_KEY`,
`RESET_SECRET_KEY` e `POSTGRES_PASSWORD`. Não reutilize credenciais de outros
sistemas e não versione esse arquivo.

```bash
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

O frontend estará em <http://localhost:8082>. O backend estará em
<http://localhost:8000>. A migration do banco roda automaticamente antes da API.

Diagnóstico e encerramento:

```bash
docker compose logs --tail=200
docker compose down
```

O volume `postgres_data` é preservado por padrão. Para remover também todos os
dados locais da aplicação:

```bash
docker compose down --volumes
```

## Atualização do ambiente local

```bash
git pull --ff-only
docker compose build --pull
docker compose up -d
```

O projeto não publica imagens em GHCR. Cada clone constrói suas próprias imagens
a partir dos Dockerfiles versionados.

## Antes de qualquer implantação real

Uma implantação externa exige, no mínimo:

1. nova auditoria da autenticação, autorização por workspace e ciclo de vida de
   tokens;
2. revisão e atualização de todas as dependências e imagens-base;
3. gerenciamento externo de segredos e rotação de qualquer credencial
   potencialmente exposta;
4. TLS, proxy reverso, política CORS e cabeçalhos ajustados ao domínio real;
5. isolamento de rede, backups testados, observabilidade e plano de recuperação;
6. fluxo de e-mail próprio, com credenciais dedicadas e sem segredos no frontend;
7. CI com versões de ações e dependências revisadas, além de análise de segurança;
8. definição de manutenção, suporte e resposta a vulnerabilidades.

O bloqueio de cadastro público e a revogação de tokens implementados no projeto
são defesas adicionais, não uma autorização para expor a aplicação.

Até esses itens serem concluídos e verificados, não encaminhe portas, não anexe
o stack a redes de proxy e não publique a aplicação na internet.
