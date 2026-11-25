# 02 — O que é o Google Borg?

## Definição

O **Borg** é um gerenciador de clusters desenvolvido pelo Google. Seu papel é coordenar a execução de trabalhos (*jobs*) distribuídos por grandes conjuntos de máquinas.

Ele ajuda a decidir **em quais máquinas** as tarefas serão executadas, a administrar os recursos disponíveis e a recuperar trabalhos quando ocorrem problemas. Os trabalhos podem incluir serviços de longa duração e tarefas de processamento em lote.

## Uma analogia útil: o maestro

Imagine uma orquestra com muitos músicos. Um maestro coordena quem toca e quando. Da mesma maneira, o Borg coordena a execução de vários programas sobre uma grande infraestrutura.

A comparação é uma **analogia didática**: o Borg não é um maestro literal e, naturalmente, possui mecanismos de escalonamento e tolerância a falhas mais complexos.

## Conceitos essenciais

| Conceito | Significado no contexto |
| --- | --- |
| **Cluster** | Grupo de máquinas administradas em conjunto |
| **Job (trabalho)** | Aplicação ou conjunto de tarefas submetidas ao Borg |
| **Escalonamento** | Escolha de onde alocar uma tarefa |
| **Disponibilidade** | Esforço para manter serviços funcionando mesmo diante de falhas |
| **Automação** | Redução da necessidade de controlar cada máquina manualmente |

No artigo técnico de 2015, os pesquisadores do Google descrevem o Borg executando centenas de milhares de trabalhos, de milhares de aplicações, em diversos clusters. Esse dado é um retrato publicado naquele ano, e **não deve ser apresentado como uma medição atual**.

## O que o Borg não resolve sozinho?

O fato de um trabalho poder ser alocado a uma máquina **não comprova, por si só, a procedência do binário e de sua configuração**. Essa verificação é tratada pelo controle de autorização integrado à infraestrutura: o BAB.

Assim, as funções são complementares:

- **Borg:** organiza e executa o trabalho.
- **BAB:** determina se o trabalho satisfaz a política de segurança para poder executar com determinada identidade de serviço.

**Fontes:** [Large-scale cluster management at Google with Borg (2015)](REFERENCIAS.md#3-large-scale-cluster-management-at-google-with-borg--artigo-cientifico) e [Binary Authorization for Borg](REFERENCIAS.md#1-binary-authorization-for-borg--google-cloud).
