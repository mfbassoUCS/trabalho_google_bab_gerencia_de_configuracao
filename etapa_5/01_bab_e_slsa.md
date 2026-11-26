# 01 --- BAB → SLSA

## Visão geral

O **Binary Authorization for Borg (BAB)** é um mecanismo interno de
segurança desenvolvido pelo Google para controlar quais softwares podem
ser executados em produção. Sua função é verificar se os softwares
passaram pelos processos necessários de revisão, construção e
autorização antes de serem implantados.

A experiência do Google com o BAB ajudou a consolidar conceitos que
foram incorporados ao **SLSA (Supply-chain Levels for Software
Artifacts)**.

## O que é o BAB?

O BAB funciona como uma camada de autorização durante a implantação de
softwares no ambiente Borg, sistema de gerenciamento de infraestrutura
utilizado pelo Google.

Antes de permitir que um serviço seja executado, o mecanismo verifica se
ele atende às políticas de segurança definidas para aquele serviço.
Entre os requisitos estão:

-   Código revisado e aprovado.
-   Build realizado por um ambiente confiável.
-   Registro de procedência do software.
-   Configurações submetidas a controle.
-   Atendimento às políticas de segurança do serviço.

Caso os requisitos não sejam atendidos, a implantação pode ser
bloqueada.

## O que é o SLSA?

O SLSA é um framework aberto que estabelece práticas e requisitos para
proteger a cadeia de suprimentos de software. Ele busca garantir que
seja possível identificar a origem do código, verificar como o software
foi construído e confirmar a integridade dos arquivos gerados.

## Qual a relação entre eles?

O BAB é uma solução interna utilizada pelo Google, enquanto o SLSA é uma
especificação aberta que permite que outras empresas adotem práticas
semelhantes.

Ambos compartilham princípios como revisão de código, builds confiáveis,
rastreabilidade e verificação de integridade.

> **Frase-chave:** O Google utiliza o BAB para controlar a execução de
> softwares em sua infraestrutura, enquanto o SLSA permite que outras
> organizações adotem princípios semelhantes.
