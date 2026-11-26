# 01 — Contexto: por que falar de autorização de binários?

## O cenário

O Google mantém serviços utilizados em grande escala. Isso demanda uma infraestrutura capaz de executar muitos programas, distribuir cargas de trabalho e realizar atualizações frequentes. O **Borg** é um dos sistemas internos que tornam essa operação possível.

Entretanto, mesmo com uma infraestrutura de execução automatizada, ainda existe outra pergunta: **como comprovar que o software enviado para produção é o software que a organização autorizou?**

## O risco que motivou o controle

Uma atualização pode ter passado pela revisão de código, mas o artefato apresentado para implantação precisa estar associado a essa origem e ao processo de construção esperado. Se a organização não consegue comprovar esse vínculo, alguém com acesso ao fluxo de entrega poderia tentar executar um binário não autorizado.

Isso é um problema da **segurança da cadeia de suprimentos de software** (*software supply chain security*): proteger a sequência que vai do código-fonte à construção e à execução do programa.

## O que é BAB, em uma frase?

**Binary Authorization for Borg (BAB)** é um mecanismo interno do Google, integrado ao Borg, para aplicar políticas de autorização a trabalhos que vão executar usando a identidade de um serviço.

Em outras palavras: a plataforma não deve confiar apenas no pedido de implantação; ela precisa de **evidências verificáveis** de que o software cumpre as regras aplicáveis.

> A proposta não é afirmar que todo software autorizado está livre de falhas, e sim impedir, como regra geral, a execução de software que não cumpra os controles de procedência e aprovação exigidos.

## Conexão com Gerência de Configuração

Este caso envolve controle de alterações, identificação de versões, rastreabilidade dos artefatos e auditoria do processo de implantação. O BAB é um exemplo de como requisitos desses processos podem ser transformados em verificações automáticas.

**Fontes:** [Binary Authorization for Borg](REFERENCIAS.md#1-binary-authorization-for-borg--google-cloud) e [How Google Does It](REFERENCIAS.md#2-how-google-does-it--google-cloud-blog).
