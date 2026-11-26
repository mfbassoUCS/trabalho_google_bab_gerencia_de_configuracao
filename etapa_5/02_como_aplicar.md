# 02 --- Como aplicar?

## Visão geral

Outras empresas podem aproveitar as práticas utilizadas pelo Google para
aumentar a segurança de seus processos de desenvolvimento, mesmo sem
possuir uma infraestrutura tão grande. A implementação pode acontecer
gradualmente, utilizando ferramentas e processos já disponíveis no
mercado.

## Principais práticas

### 1. Revisão de código

Exigir que alterações sejam revisadas e aprovadas por outro
desenvolvedor antes de serem incorporadas ao projeto. Isso reduz o risco
de alterações maliciosas ou não autorizadas.

Ferramentas possíveis: GitHub Pull Requests, GitLab Merge Requests e
regras de proteção de branches.

### 2. Pipelines CI/CD confiáveis

Utilizar ferramentas como GitHub Actions, GitLab CI/CD ou Jenkins para
automatizar a compilação, os testes e a publicação das aplicações. Os
processos devem ocorrer em ambientes controlados.

### 3. Assinaturas digitais e procedência

Gerar registros que comprovem como o software foi construído, qual
código foi utilizado e quais dependências participaram do processo. As
assinaturas digitais ajudam a verificar a autenticidade e a integridade
dos artefatos.

### 4. Verificações de segurança

Realizar análises de vulnerabilidades, testes automatizados e
verificações das dependências antes de permitir que uma aplicação chegue
à produção.

### 5. Bloqueio de versões não autorizadas

Configurar políticas para impedir a publicação de softwares que não
atendam aos requisitos de segurança estabelecidos.

## Exemplo prático

Uma empresa pode configurar seu pipeline para exigir uma aprovação de
código, executar testes automatizados, verificar vulnerabilidades e
gerar uma assinatura digital do software. Se alguma dessas etapas
obrigatórias falhar, a publicação poderá ser bloqueada.

> **Frase-chave:** Mesmo sem a infraestrutura do Google, qualquer
> empresa pode melhorar sua segurança utilizando revisão de código,
> builds confiáveis e verificações automatizadas.
