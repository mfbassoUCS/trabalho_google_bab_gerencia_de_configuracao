# 03 --- Prós e contras

## Visão geral

A adoção de práticas baseadas no BAB e no SLSA proporciona benefícios
importantes para a segurança dos softwares. Entretanto, também existem
limitações que precisam ser consideradas durante a implementação.

## Benefícios

-   **Maior segurança na cadeia de suprimentos:** reduz os riscos de
    softwares adulterados chegarem à produção.
-   **Rastreabilidade das alterações e versões:** permite identificar a
    origem do código e acompanhar as mudanças realizadas.
-   **Redução de alterações não autorizadas:** dificulta modificações
    que não passaram pelos processos de aprovação.
-   **Automação das verificações de segurança:** reduz a dependência de
    processos manuais e facilita auditorias.

## Ataques que ajudam a prevenir

-   **Comprometimento do pipeline CI/CD:** builds confiáveis e
    verificações de procedência ajudam a identificar resultados não
    autorizados.
-   **Inserção de código malicioso:** revisões obrigatórias e controles
    de acesso dificultam a introdução de alterações não aprovadas.
-   **Alteração de binários após a compilação:** assinaturas e hashes
    ajudam a identificar modificações nos arquivos.
-   **Publicação de softwares não autorizados:** políticas de segurança
    podem bloquear aplicações que não atendam aos requisitos.

## Limitações

-   **Custo e complexidade de implementação:** exige investimento em
    ferramentas, infraestrutura e treinamento.
-   **Necessidade de infraestrutura confiável:** os sistemas
    responsáveis por compilar e verificar os softwares também precisam
    ser protegidos.
-   **Não elimina todas as vulnerabilidades:** um software pode passar
    pelas verificações e ainda apresentar falhas.
-   **Dependências externas:** bibliotecas de terceiros podem conter
    vulnerabilidades ou códigos maliciosos.

## Ponto importante

O BAB possui mecanismos de exceção para situações emergenciais,
permitindo que determinadas implantações ocorram fora do fluxo habitual
mediante justificativa e registro. Isso demonstra que a segurança
precisa ser equilibrada com a disponibilidade dos serviços.

> **Frase-chave:** Essas práticas reduzem os riscos de ataques à cadeia
> de suprimentos, mas não garantem que um software esteja completamente
> livre de vulnerabilidades.
