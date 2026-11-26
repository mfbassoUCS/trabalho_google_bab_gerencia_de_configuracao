# Binary Authorization for Borg (BAB) — Grupo B

**Trabalho 2 · Gerência de Configuração (UCS) · Google: só roda em produção o que tem procedência comprovada**

O **Binary Authorization for Borg (BAB)** é um controle interno do Google, integrado ao Borg, que exige evidências verificáveis antes de um job executar com a identidade de um serviço: código revisado, build oficial e configuração revisada. Os conceitos do BAB foram incorporados ao framework aberto **SLSA**.

Este repositório reúne o material da apresentação para a turma consultar posteriormente.

## Organização

Cada parte da apresentação tem uma pasta própria, com **um arquivo por slide** e um `REFERENCIAS.md` com as fontes daquela parte.

| Parte | Tempo | Tema | Material |
| --- | --- | --- | --- |
| **1** | 0:00 – 4:00 | Contexto, Google Borg e o problema de procedência | [etapa_1](etapa_1/) |
| **2** | 4:00 – 8:00 | Como funciona o Binary Authorization for Borg | [etapa_2](etapa_2/) |
| **3** | 8:00 – 12:00 | Demonstração prática | _a fazer_ |
| **4** | 12:00 – 16:00 | Relação com Gerência de Configuração | _a fazer_ |
| **5** | 16:00 – 20:00 | SLSA, benefícios, limitações e conclusão | _a fazer_ |

## Parte 1 — Contexto e problema

- [01 — Contexto: por que falar de autorização de binários?](etapa_1/01-contexto.md)
- [02 — O que é o Google Borg?](etapa_1/02-google-borg.md)
- [03 — O problema: o binário enviado é realmente o autorizado?](etapa_1/03-problema-de-procedencia.md)
- [04 — A solução: Binary Authorization for Borg](etapa_1/04-introducao-ao-bab.md)
- [Referências da Parte 1](etapa_1/REFERENCIAS.md)

## Parte 2 — Como funciona o BAB

- [05 — Do commit à produção: as quatro etapas obrigatórias](etapa_2/05-o-caminho-ate-producao.md)
- [06 — A prova: procedência (*provenance*) do build](etapa_2/06-procedencia.md)
- [07 — A regra: política específica do serviço](etapa_2/07-politica-do-servico.md)
- [08 — A verificação: Borg Prime, BAB e os modos de aplicação](etapa_2/08-verificacao-no-deploy.md)
- [Referências da Parte 2](etapa_2/REFERENCIAS.md)
