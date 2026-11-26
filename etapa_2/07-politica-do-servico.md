# 07 — A regra: política específica do serviço

## Definição

Quando os proprietários de um serviço adotam o BAB, eles criam uma **política específica do serviço** (*service-specific policy*). Ela define **qual código e qual configuração** podem executar com a identidade daquele serviço, e quais propriedades esse código e essa configuração precisam ter.

Todos os jobs que executam com a identidade do serviço precisam cumprir essa política. Segundo a documentação do Google, **todos os serviços do Borg** precisam configurar uma.

## Requisitos padrão

Por padrão, a política exige:

| Requisito | Significado |
| --- | --- |
| **Código auditável** | É possível rastrear a imagem do contêiner até o código-fonte legível, por meio da procedência. Uma política de retenção mantém esse código por **pelo menos 18 meses**, mesmo que ele não tenha sido enviado ao repositório. |
| **Código enviado ao repositório** | O código foi construído a partir de um local definido do repositório oficial. Em geral, isso significa que passou por revisão. |
| **Configuração enviada ao repositório** | Toda configuração fornecida no deploy passa pelo mesmo processo de revisão e envio do código. Valores, argumentos e flags de linha de comando não podem ser alterados sem revisão. |

O terceiro requisito é especialmente relevante para Gerência de Configuração: um binário aprovado pode mudar de comportamento por meio de parâmetros. Por isso, **a configuração também é tratada como item controlado**.

## A política também é código

Definir ou alterar uma política é uma **mudança de código que precisa ser revisada**. Assim, nenhuma pessoa consegue afrouxar sozinha as regras do próprio serviço.

## Por que a regra fica ligada à identidade, e não ao binário?

É difícil definir uma política completa para um software sem saber **onde ele será executado** e **quais dados acessará**. Por isso, a política é definida em termos de uma **identidade de execução**, e não do binário.

Consequências:

- O mesmo código pode executar em ambientes diferentes, sujeito a políticas diferentes.
- A verificação acontece **quando o código é implantado e acessa dados**, e não quando ele é construído.

## Controle proporcional ao risco

As exigências não são iguais para todos os serviços:

- Serviços **com acesso a dados de usuários** ou a outras informações confidenciais precisam da proteção do BAB.
- Jobs de **desenvolvimento e controle de qualidade** sem acesso a dados sensíveis podem executar com menos controles.
- Em **casos raros**, serviços com uma exceção válida e aprovada podem ter uma política mais permissiva, como uma que exija apenas auditoria.

Portanto, não é correto afirmar que todos os serviços do Google seguem exatamente a mesma regra.

## Exemplo ilustrativo

```yaml
# política do serviço "pagamentos" (ilustrativo)
identidade: pagamentos-prod
exigir:
  codigo_auditavel: true    # imagem -> procedência -> código-fonte
  codigo_enviado: true      # build a partir de //pagamentos no repositório
  config_enviada: true      # flags e argumentos também revisados
builders_confiaveis:
  - build-oficial           # só a procedência assinada por ele é aceita
```

**Atenção:** esse é um **exemplo ilustrativo**. A documentação do Google descreve os requisitos, mas não publica o formato interno das políticas.

## Frase-chave para a apresentação

> **A regra fica presa à identidade do serviço, não ao binário, e mudar a regra também exige revisão.**

**Fontes:** [Binary Authorization for Borg](REFERENCIAS.md#1-binary-authorization-for-borg--google-cloud) e [Building Secure and Reliable Systems](REFERENCIAS.md#3-building-secure-and-reliable-systems--livro).
