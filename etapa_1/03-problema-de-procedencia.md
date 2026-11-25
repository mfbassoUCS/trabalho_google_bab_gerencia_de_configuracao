# 03 — O problema: o binário enviado é realmente o autorizado?

## Um exemplo hipotético

1. Um desenvolvedor altera um programa e envia o código para revisão.
2. O código é revisado e aceito segundo o processo da equipe.
3. Um sistema de build gera o binário correspondente.
4. Na implantação, alguém tenta substituir o artefato esperado por outro arquivo, que não possui procedência aprovada.
5. Sem uma verificação apropriada, a infraestrutura poderia executar esse arquivo apenas porque a solicitação partiu de alguém com permissão para implantar.

**Atenção:** esse é um **cenário ilustrativo**, não o relato de um incidente ocorrido no Google.

## Por que isso importa?

Existem riscos distintos:

- **Origem desconhecida:** não se sabe de qual código-fonte surgiu o binário.
- **Build não verificável:** não se consegue demonstrar qual sistema e quais insumos produziram o artefato.
- **Alteração posterior:** o arquivo implantado pode ser diferente daquele produzido e registrado pelo build.
- **Configuração não revisada:** parâmetros ou configurações podem mudar o comportamento de um serviço, mesmo sem alteração no binário.

A identidade de quem solicita o deploy, isoladamente, **não demonstra que o artefato está autorizado**. É preciso estabelecer o vínculo entre a versão, o processo de construção, a configuração e as regras do serviço.

## Procedência não é ausência de vulnerabilidades

Verificar procedência não significa provar que um programa é perfeito. Um binário autorizado ainda pode conter bugs ou vulnerabilidades. A principal garantia aqui é a respeito de **origem, integridade e conformidade com a política aplicável**, não da qualidade absoluta do software.

## Pergunta de transição

> Se um programa pode chegar à produção por um processo automatizado, como exigir evidências confiáveis antes de permitir sua execução?

É essa questão que introduz o **Binary Authorization for Borg**.

**Fontes:** [Binary Authorization for Borg](REFERENCIAS.md#1-binary-authorization-for-borg--google-cloud) e [How Google Does It](REFERENCIAS.md#2-how-google-does-it--google-cloud-blog).
