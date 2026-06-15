# Estrutura de Dados: Documento

Estrutura utilizada para inclusão de documentos nos endpoints `gerarProcedimento` e `incluirDocumento`.

---

## Campos

| Campo | Tipo | Obrigatoriedade | Descrição |
|---|---|---|---|
| `Tipo` | string | Obrigatório | `G` = gerado internamente / `R` = recebido (externo) |
| `IdProcedimento` | string | Condicional | ID interno do processo onde o documento será inserido. Passar `null` quando o documento está sendo gerado junto com o processo em `gerarProcedimento` |
| `ProtocoloProcedimento` | string | Condicional | Número do processo visível para o usuário. Alternativa ao `IdProcedimento` |
| `IdSerie` | string | Obrigatório | ID do tipo de documento (série) no SEI |
| `Numero` | string | Condicional | Número do documento. Passar `null` para documentos gerados com numeração controlada pelo SEI. Obrigatório para documentos externos |
| `NomeArvore` | string | Opcional | Nome complementar exibido na árvore de documentos do processo |
| `DinValor` | string | Opcional | Valor monetário associado ao documento, ex: `133.050,95` |
| `Data` | string | Condicional | Data do documento. **Obrigatório para documentos externos.** Passar `null` para documentos gerados |
| `Descricao` | string | Opcional | Descrição do documento gerado. Passar `null` para documentos externos |
| `IdTipoConferencia` | string | Condicional | ID do tipo de conferência. Aplicável apenas a documentos externos |
| `SinArquivamento` | S/N | Opcional | Indica se o documento deve ser arquivado |
| `Remetente` | objeto | Condicional | **Obrigatório para documentos externos.** Passar `null` para documentos gerados (ver estrutura `Remetente`) |
| `Interessados` | lista | Opcional | Conjunto de interessados do documento (ver estrutura `Interessado`) |
| `Destinatarios` | lista | Opcional | Conjunto de destinatários do documento (ver estrutura `Destinatario`) |
| `Observacao` | string | Opcional | Texto de observação da unidade. Passar `null` se não houver |
| `NomeArquivo` | string | Condicional | Nome do arquivo. **Obrigatório para documentos externos.** Passar `null` para documentos gerados |
| `NivelAcesso` | string | Opcional | `0` = público / `1` = restrito / `2` = sigiloso / `null` = herda o nível sugerido para o tipo de processo |
| `IdHipoteseLegal` | string | Condicional | ID da hipótese legal associada. Obrigatório quando `NivelAcesso` for `1` ou `2` |
| `Conteudo` | string | Condicional | Conteúdo do documento codificado em **Base64**. Para documentos gerados (`G`): fragmento HTML do corpo. Para documentos externos (`R`): conteúdo binário do arquivo |
| `ConteudoSecoes` | lista | Opcional | Conteúdos das seções do documento em Base64 (ver estrutura `SecaoDocumento`). Apenas para documentos gerados com seções nomeadas no modelo |
| `ConteudoMTOM` | binário | Condicional | Conteúdo binário via MTOM. Apenas para documentos externos. Mutuamente exclusivo com `Conteudo` |
| `IdArquivo` | string | Opcional | ID de arquivo pré-enviado via `adicionarArquivo`. Alternativa ao `Conteudo` para documentos externos grandes |
| `Campos` | lista | Opcional | Campos de formulário associados ao documento (ver estrutura `Campo`) |
| `SinBloqueado` | S/N | Opcional | `S` = bloqueia o documento contra exclusão e alteração de conteúdo |
| `IdItemEtapa` | string | Opcional | ID para associação do documento com um item do Plano de Trabalho |

---

## Documento Gerado (Tipo G)

Usado para criar documentos internos editáveis no SEI, gerados a partir de um modelo/template da série.

```python
import base64

conteudo_html = "<p class=\"Texto_Justificado_Recuo_Primeira_Linha\">Texto do documento.</p>"
conteudo_b64  = base64.b64encode(conteudo_html.encode("iso-8859-1")).decode("utf-8")

documento_gerado = {
    'Tipo':        'G',
    'IdSerie':     '290',       # 290 = Ofício
    'NivelAcesso': '0',
    'Conteudo':    conteudo_b64,
}
```

### Observações sobre o campo `Conteudo` para documentos gerados

- Deve conter apenas o **fragmento HTML do corpo** do documento — sem `<html>`, `<head>` ou `<body>`
- O SEI injeta automaticamente o template da série (cabeçalho, rodapé, campos do modelo)
- O conteúdo deve ser codificado em **iso-8859-1** antes do Base64, pois é o charset padrão do SEI
- Se o modelo da série tiver **seções nomeadas** (ex: Ementa, Corpo do Texto), usar `ConteudoSecoes` no lugar de `Conteudo`

---

## Documento Recebido (Tipo R)

Usado para registrar documentos externos recebidos (ex: ofícios, petições, arquivos digitalizados).

```python
documento_externo = {
    'Tipo':              'R',
    'IdSerie':           '290',
    'Numero':            '1000',
    'Data':              '15/06/2026',
    'Descricao':         'Ofício recebido',
    'NomeArquivo':       'oficio.pdf',
    'Remetente':         {'Sigla': 'SIGLA', 'Nome': 'Nome do Remetente'},
    'Interessados':      [{'Nome': 'Nome do Interessado'}],
    'Destinatarios':     [],
    'NivelAcesso':       '0',
    'Conteudo':          conteudo_b64,  # conteúdo binário do arquivo em Base64
}
```

---

## Estrutura SecaoDocumento

Utilizada no campo `ConteudoSecoes` para modelos com seções nomeadas:

```python
secoes = [
    {
        'Nome':     'Ementa',
        'Conteudo': base64.b64encode('Texto da ementa'.encode('iso-8859-1')).decode('utf-8')
    },
    {
        'Nome':     'Corpo do Texto',
        'Conteudo': base64.b64encode('Texto principal'.encode('iso-8859-1')).decode('utf-8')
    },
]

documento_com_secoes = {
    'Tipo':            'G',
    'IdSerie':         '290',
    'NivelAcesso':     '0',
    'ConteudoSecoes':  secoes,
}
```

---

## Identificação de Interessados e Destinatários

O SEI tenta identificar os contatos na seguinte ordem de prioridade:

1. `IdContato`
2. `Cpf`
3. `Cnpj`
4. `Sigla` + `Nome`
5. `Sigla`
6. `Nome`

Se o contato não for encontrado, ele será **cadastrado automaticamente** com os dados fornecidos. Por isso, é recomendável sempre informar o `Nome` para permitir o cadastro automático caso necessário.

---

## Observações Gerais

- `IdProcedimento` e `ProtocoloProcedimento` são mutuamente opcionais — basta informar um dos dois quando incluindo documento em processo existente
- `Conteudo` e `ConteudoMTOM` são mutuamente exclusivos para documentos externos
- `Conteudo` e `IdArquivo` são mutuamente exclusivos — se o arquivo foi pré-enviado via `adicionarArquivo`, não é necessário informar `Conteudo`
