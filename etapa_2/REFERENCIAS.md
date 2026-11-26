# Referências — Parte 2

As referências abaixo sustentam a explicação das quatro etapas obrigatórias, da procedência gerada pelo build, da política específica do serviço e da verificação feita pelo Borg Prime e pelo BAB.

## 1. Binary Authorization for Borg — Google Cloud

**Instituição:** Google Cloud / Google Security

**Título:** *Binary Authorization for Borg*

**Documento:** documentação técnica oficial (whitepaper).

**URL:** https://docs.cloud.google.com/docs/security/binary-authorization-for-borg

**Utilizado para:** as quatro etapas do processo de desenvolvimento e produção, conteúdo da procedência, isolamento do sistema de build, requisitos padrão da política específica do serviço, retenção de 18 meses, papel do Borg Prime como autoridade certificadora do ALTS, modos de aplicação, procedimento de emergência e automação de conformidade (SOX).

## 2. How Google Does It — Google Cloud Blog

**Autores:** Daniel Lees e Anton Chuvakin

**Título:** *How Google Does It: Using Binary Authorization to boost supply chain security*

**Publicado em:** 21 de novembro de 2025.

**URL:** https://cloud.google.com/transform/how-google-does-it-using-binary-authorization-to-boost-supply-chain-security

**Utilizado para:** princípio "não confie, verifique", bloqueio de implantações que não cumprem a política e trilha de auditoria.

## 3. Building Secure and Reliable Systems — livro

**Autores:** Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea e Adam Stubblefield.

**Título:** *Building Secure and Reliable Systems: Best Practices for Designing, Implementing, and Maintaining Systems*

**Editora:** O'Reilly Media, 2020. Disponível gratuitamente pelo Google.

**URL do capítulo 14 (*Deploying Code*):** https://google.github.io/building-secure-and-reliable-systems/raw/ch14.html

**Utilizado para:** ideia de verificar o artefato, e não apenas quem faz o deploy (seção *Verify Artifacts, Not Just People*); configuração tratada como código (*Treat Configuration as Code*); procedência de binários, políticas de deploy baseadas em procedência e builds verificáveis.

## 4. SLSA Provenance — slsa.dev

**Instituição:** OpenSSF / projeto SLSA

**Título:** *SLSA Provenance* (especificação v1.0)

**URL:** https://slsa.dev/spec/v1.0/provenance

**Utilizado para:** formato aberto de procedência usado no exemplo ilustrativo do arquivo 06 (campos `subject`, `buildDefinition`, `resolvedDependencies` e `builder.id`).

## 5. Application Layer Transport Security (ALTS) — Google Cloud

**Instituição:** Google Cloud

**Título:** *Application Layer Transport Security*

**URL:** https://docs.cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security

**Utilizado para:** o que é o ALTS e por que o certificado emitido pelo Borg Prime é necessário para que um job se autentique e acesse outros serviços.

## 6. BeyondProd — Google Cloud

**Instituição:** Google Cloud

**Título:** *BeyondProd*

**Documento:** documentação técnica oficial (whitepaper).

**URL:** https://docs.cloud.google.com/docs/security/beyondprod

**Utilizado para:** contexto do BAB como parte de um modelo maior de segurança para microsserviços, baseado em identidade de serviço e implantação controlada.

## Observações para quem reutilizar o material

- Os exemplos de **procedência (JSON)** e de **política (YAML)** são **ilustrativos**. O Google não publica o formato interno usado pelo BAB.
- A tradução automática em português da documentação oficial diz que o Borg Prime é "autoridade certificadora do **Pub/Sub**"; o original em inglês diz **ALTS**.
- A retenção de **18 meses** se refere ao código-fonte legível usado nos builds, não aos binários.
- O cálculo de hash e a verificação de assinatura são **demonstrados na Parte 3**; esta parte explica apenas o papel de cada um na procedência.
- **BAB (interno do Google)** e o produto **Binary Authorization do Google Cloud** compartilham ideias, mas não são o mesmo sistema.
