# 10 — As 3 perguntas do Borg

## Visão geral

Na demo, a política do serviço foi resumida em três perguntas. O Borg só libera o deploy se **todas** tiverem resposta "sim".

| # | Pergunta | O que ela garante |
| --- | --- | --- |
| **1** | O selo foi assinado pelo **build oficial**? | O programa foi construído no lugar certo, e não no computador de alguém. |
| **2** | O programa é **igual** ao descrito no selo? | Ninguém alterou o programa depois do build. |
| **3** | O código foi **revisado** por outra pessoa? | Ninguém levou código à produção sozinho. |

**Três vezes sim → PERMITIDO. Qualquer não → NEGADO.**

## Relação com a política real

A política específica de serviço do Google (ver [slide 07](../etapa_2/07-politica-do-servico.md)) exige código auditável, código submetido e configuração submetida. As três perguntas da demo são uma simplificação didática dessas exigências. A verificação da configuração (flags) não foi incluída na versão em navegador, mas existe na versão de terminal.
