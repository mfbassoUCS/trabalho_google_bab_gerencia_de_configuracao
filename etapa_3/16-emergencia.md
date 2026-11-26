# 16 — E numa emergência?

## Visão geral

Às 3h da manhã, com o serviço fora do ar, não dá para esperar uma revisão. Um controle de segurança que impede apagar incêndio não sobrevive na prática, por isso o BAB tem um procedimento de emergência (*break-glass*).

| # | Mecanismo | O que faz |
| --- | --- | --- |
| **1** | **Break-glass** | Permite forçar o deploy, mas exige uma **justificativa**. |
| **2** | **Alerta** | O job fica registrado e a **equipe de segurança** e os donos do serviço são avisados. |
| **3** | **Verificação contínua** | Pelo menos uma vez por dia, o BAB reconfere os jobs em execução e cobra a regularização. |

**Flexível na emergência, mas nada fica escondido.**

A versão de terminal da demo ([`demo-terminal/`](demo-terminal/), `python demo.py --completa`) simula esse fluxo: o deploy é forçado, a verificação contínua aponta o job como não conforme e, depois da revisão, ele volta a ficar conforme.

## Fechamento da demonstração

Foram quatro tentativas e só uma passou. Cada tentativa barrada falhou numa pergunta diferente, e em todas elas a pessoa **tinha permissão de deploy**.

> O Borg não pergunta **quem é você**. Ele pergunta **de onde veio esse programa**.
