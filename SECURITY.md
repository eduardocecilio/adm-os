# Política de segurança

## Status

O AdmOS está arquivado, sem versões suportadas, manutenção ativa ou SLA de
segurança. O Compose fornecido serve apenas para demonstração local em
`127.0.0.1`. Este código não deve processar dados reais nem ser exposto à
internet.

## Limites conhecidos

- O desenho de autenticação, convites e papéis de workspace precisa de nova
  revisão antes de qualquer uso real. Cadastro sem convite é bloqueado fora de
  localhost por padrão.
- Tokens de acesso duram uma hora, ficam somente no `sessionStorage` e são
  revogados quando a senha ou o e-mail muda. O armazenamento continua acessível
  ao JavaScript; qualquer implantação real deve preferir sessões com cookies
  `HttpOnly` e proteção CSRF.
- Tokens de redefinição duram 30 minutos e se tornam inválidos após o primeiro
  uso. Todo valor `VITE_*` fica público no JavaScript compilado.
- A demonstração usa HTTP local e não fornece TLS, backup, monitoramento,
  recuperação ou gerenciamento externo de segredos.
- A integração de e-mail via webhook é opcional e vem desativada. Ao testá-la,
  use uma credencial dedicada e nunca a coloque no código ou em `VITE_*`.
- Dependências e imagens-base podem ficar desatualizadas porque o projeto não é
  mantido.

## Segredos e histórico

Os campos secretos do `.env.example` ficam vazios, o `.gitignore` bloqueia
variantes de arquivos de ambiente por padrão e o Compose recusa iniciar sem
valores explícitos. Isso não substitui rotação: qualquer credencial que tenha
aparecido em outro repositório, commit, log ou ambiente deve ser tratada como
comprometida e revogada antes da publicação deste snapshot.

Nunca envie banco de dados, dados pessoais, dumps, tokens, chaves privadas ou um
`.env` preenchido em issues, pull requests ou commits.

## Relato responsável

Não publique detalhes exploráveis ou segredos em uma issue. Se o repositório
oferecer **Private vulnerability reporting**, use a opção de relatar uma
vulnerabilidade na aba Security. Caso contrário, contate o mantenedor pelo canal
privado indicado no perfil do repositório.

Como o projeto está arquivado, um relato pode ser documentado sem resultar em
correção ou nova versão.
