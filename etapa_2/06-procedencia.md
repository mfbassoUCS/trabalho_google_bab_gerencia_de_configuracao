# 06 — A prova: procedência (*provenance*) do build

## Definição

**Procedência** (*provenance*) é um certificado **assinado digitalmente** que o sistema de build oficial gera a cada build. Ele descreve de onde o artefato veio e como foi produzido.

Uma analogia útil é o **RG do binário**: um documento emitido por uma autoridade confiável, que identifica o programa e permite conferir se ele é quem diz ser. Trata-se de uma **analogia didática**; a procedência é um registro técnico, não um documento de identidade.

## O que a procedência registra

Segundo a documentação do Google, o certificado contém:

| Informação | Conteúdo | Para que serve |
| --- | --- | --- |
| **Fontes e dependências** | O código-fonte e as dependências que entraram no build | Ligar o binário ao commit e, por consequência, à revisão |
| **Hashes criptográficos** | A "impressão digital" do binário e de outros artefatos | Detectar qualquer alteração posterior no arquivo |
| **Parâmetros do build** | Os parâmetros completos usados na construção | Saber exatamente como o artefato foi produzido |
| **Assinatura** | Assinatura do sistema de build oficial | Garantir que o certificado foi emitido pelo build confiável |

## O que a procedência permite

1. **Rastrear** um binário até o código-fonte usado para criá-lo. Por extensão, também é possível rastrear o processo de criação e envio desse código, incluindo a revisão.
2. **Verificar** que o binário não foi modificado: qualquer alteração no arquivo invalida automaticamente a correspondência com a assinatura.

## Hash, assinatura e procedência não são a mesma coisa

| Conceito | Responde a qual pergunta? |
| --- | --- |
| **Hash** | Este arquivo é exatamente o mesmo que foi produzido? |
| **Assinatura digital** | Quem garante essa informação, e ela foi alterada? |
| **Procedência** | De onde o artefato veio, com quais insumos e por qual processo? |

A procedência **usa** hashes e assinatura, mas é o documento completo que reúne essas informações. O cálculo do hash e a verificação da assinatura são demonstrados na prática na Parte 3.

## Por que o build precisa ser isolado?

O sistema de build do Google executa em um ambiente **isolado e bloqueado**, separado dos funcionários que solicitam os builds. Como as ações de build podem executar código arbitrário, o sistema também foi reforçado para **multilocação**: um build não deve conseguir influenciar outro, nem comprometer a integridade dos manifestos de procedência ou do próprio sistema.

Se qualquer pessoa pudesse produzir uma procedência válida no próprio computador, o certificado não provaria nada. A confiança está no **build oficial**, não em quem pediu o build.

## Exemplo no formato aberto SLSA

O formato interno usado pelo Google não é público. Entretanto, os conceitos do BAB foram incorporados ao framework aberto **SLSA**, que define um formato de procedência. Um exemplo **simplificado** nesse estilo:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    { "name": "servico-pagamentos", "digest": { "sha256": "9f2c...e41a" } }
  ],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "https://exemplo.com/build-oficial/v1",
      "externalParameters": { "alvo": "//pagamentos:servidor" },
      "resolvedDependencies": [
        { "uri": "git+monorepo", "digest": { "gitCommit": "a1b2c3..." } }
      ]
    },
    "runDetails": {
      "builder": { "id": "https://exemplo.com/build-oficial" }
    }
  }
}
```

| Campo | Significado |
| --- | --- |
| `subject.digest` | Hash do binário |
| `resolvedDependencies` | Commit de origem, que permite chegar à revisão |
| `builder.id` | Sistema que realizou o build; só é aceito se for o build oficial |

**Atenção:** esse é um **exemplo ilustrativo**, com nomes e valores fictícios. Não representa o formato interno do Google.

## Frase-chave para a apresentação

> **Não basta verificar QUEM faz o deploy: é preciso provar O QUE vai executar.**

A ideia aparece no livro *Building Secure and Reliable Systems*, do Google: verificar apenas quem iniciou a implantação não é suficiente, porque essa pessoa pode cometer um erro ou implantar uma mudança maliciosa de propósito.

**Fontes:** [Binary Authorization for Borg](REFERENCIAS.md#1-binary-authorization-for-borg--google-cloud), [Building Secure and Reliable Systems](REFERENCIAS.md#3-building-secure-and-reliable-systems--livro) e [SLSA Provenance](REFERENCIAS.md#4-slsa-provenance--slsadev).
