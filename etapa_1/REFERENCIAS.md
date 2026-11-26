# Referências — Parte 1

As referências abaixo sustentam a introdução, a descrição do Borg, o problema de procedência e a visão geral do BAB.

## 1. Binary Authorization for Borg — Google Cloud

**Instituição:** Google Cloud / Google Security

**Título:** *Binary Authorization for Borg*

**Documento:** documentação técnica oficial, com atualização informada em setembro de 2026.

**URL:** https://docs.cloud.google.com/docs/security/binary-authorization-for-borg

**Utilizado para:** objetivo do BAB, políticas por identidade de serviço, revisão, builds verificáveis, dados de procedência, autorização durante deploy, verificação contínua e exceções de emergência.

## 2. How Google Does It — Google Cloud Blog

**Autores:** Daniel Lees e Anton Chuvakin

**Título:** *How Google Does It: Using Binary Authorization to boost supply chain security*

**Publicado em:** 21 de novembro de 2025.

**URL:** https://cloud.google.com/transform/how-google-does-it-using-binary-authorization-to-boost-supply-chain-security

**Utilizado para:** motivação do controle, explicação acessível do risco de executar artefatos não autorizados e conceito de checagens por políticas.

## 3. Large-scale cluster management at Google with Borg — artigo científico

**Autores:** Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune e John Wilkes.

**Título:** *Large-scale cluster management at Google with Borg*

**Evento:** EuroSys, 2015.

**URL do artigo:** https://research.google.com/pubs/archive/43438.pdf

**Utilizado para:** conceito de gerenciador de clusters, escalonamento de workloads, arquitetura geral do Borg e desafios de escala. **Os números de escala descritos no artigo são históricos (2015).**

## 4. How Google protects its production services — Google Cloud

**Instituição:** Google Cloud

**Título:** *How Google protects its production services*

**URL:** https://docs.cloud.google.com/docs/security/production-services-protection

**Utilizado para:** papel da revisão de código e dos builds verificáveis na proteção de serviços em produção.

## Observações para quem reutilizar o material

- **BAB (interno do Google)** e o produto **Binary Authorization do Google Cloud** compartilham ideias, mas não são o mesmo sistema.
- **Borg** é o sistema de gerenciamento de clusters; **BAB** implementa verificações de autorização integradas a ele.
- O exemplo de binário substituído é **hipotético** e não deve ser atribuído a um incidente real.
- Assinaturas e procedência verificável não garantem, por si sós, que o software esteja livre de bugs.
