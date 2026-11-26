# Referências — Parte 3

As referências abaixo sustentam a demonstração prática: o fluxo de revisão, build e verificação, o conteúdo da procedência, o procedimento de emergência e os formatos usados na versão de terminal.

## 1. Binary Authorization for Borg — Google Cloud

**Instituição:** Google Cloud / Google Security

**Documento:** documentação técnica oficial (whitepaper).

**URL:** https://docs.cloud.google.com/docs/security/binary-authorization-for-borg

**Utilizado para:** as três checagens simuladas (código revisado, build verificável, integridade do binário), a emissão da credencial pelo Borg Prime, a verificação contínua e o procedimento de emergência (*break-glass*).

## 2. How Google Does It — Google Cloud Blog

**Autores:** Daniel Lees e Anton Chuvakin

**Publicado em:** 21 de novembro de 2025.

**URL:** https://cloud.google.com/transform/how-google-does-it-using-binary-authorization-to-boost-supply-chain-security

**Utilizado para:** atestados assinados por etapa do pipeline, bloqueio de deploy de imagens não conformes e o princípio "não confie, verifique".

## 3. SLSA — Supply-chain Levels for Software Artifacts

**URL:** https://slsa.dev/

**Utilizado para:** formato de proveniência v1 gerado pela versão de terminal da demo.

## 4. in-toto Attestation Framework e DSSE

**URLs:** https://github.com/in-toto/attestation e https://github.com/secure-systems-lab/dsse

**Utilizado para:** estrutura do atestado (*in-toto Statement*) e envelope de assinatura usados na versão de terminal.

## 5. Web Crypto API — MDN

**URL:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API

**Utilizado para:** cálculo do hash SHA-256 e da assinatura ECDSA na versão em navegador.
