# gerarProcedimento

Cria um novo processo no SEI, opcionalmente já incluindo documentos junto à geração.

---

## Parâmetros de Entrada

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `SiglaSistema` | string | Sigla do sistema cadastrado no SEI |
| `IdentificacaoServico` | string | Chave de acesso do serviço |
| `IdUnidade` | string | ID da unidade geradora |
| `Procedimento` | objeto | Dados do processo (ver estrutura abaixo) |
| `Documentos` | lista | Documentos a incluir na geração (pode ser lista vazia) |
| `ProcedimentosRelacionados` | lista/Nil | IDs de processos a relacionar automaticamente |
| `UnidadesEnvio` | lista/Nil | IDs de unidades para envio após geração |
| `SinManterAbertoUnidade` | S/N | Manter processo aberto na unidade de origem |
| `SinEnviarEmailNotificacao` | S/N | Enviar e-mail de aviso para unidades destinatárias |
| `DataRetornoProgramado` | string | Data para retorno programado (vazio = sem retorno) |
| `DiasRetornoProgramado` | string | Dias para retorno programado |
| `SinDiasUteisRetornoProgramado` | S/N | Se os dias de retorno são úteis |
| `IdMarcador` | string | ID de marcador da unidade (opcional) |
| `TextoMarcador` | string | Texto do marcador (opcional) |
| `DataControlePrazo` | string | Data para controle de prazo (vazio = sem prazo) |
| `DiasControlePrazo` | string | Dias para controle de prazo |
| `SinDiasUteisControlePrazo` | S/N | Se os dias de prazo são úteis |

---

## Estrutura do Procedimento

```python
novo_processo = {
    "IdTipoProcedimento": "100000358",       # ID do tipo de processo no SEI
    "Especificacao": "Descrição do processo",
    "Assuntos": {"items": [{"CodigoEstruturado": "06.10.01.07"}]},
    "Interessados": [{"Sigla": "SIGLA", "Nome": "Nome do Interessado"}],
    "Observacao": "Observação da unidade",
    "NivelAcesso": "0",                      # 0=público, 1=restrito, 2=sigiloso
}
```

---

## Estrutura do Documento (Tipo G — Gerado Internamente)

```python
documento_oficio = {
    'Tipo':        'G',         # G = gerado, R = recebido (externo)
    'IdSerie':     '290',       # ID da série (tipo de documento). 290 = Ofício
    'NivelAcesso': '0',         # 0=público, 1=restrito, 2=sigiloso
    'Conteudo':    conteudo_b64 # HTML do corpo do documento codificado em Base64 (iso-8859-1)
}
```

### Observações sobre o campo `Conteudo`

- Obrigatório para documentos do tipo `G`
- Deve conter apenas o **fragmento HTML do corpo** do documento — não incluir `<html>`, `<head>` ou `<body>`
- O SEI injeta automaticamente o template da série (cabeçalho, rodapé, campos do modelo)
- O conteúdo deve ser codificado em **iso-8859-1** antes do Base64

```python
conteudo_html = "<p class=\"Texto_Justificado_Recuo_Primeira_Linha\">Texto do documento</p>"
conteudo_b64  = base64.b64encode(conteudo_html.encode("iso-8859-1")).decode("utf-8")
```

---

## Retorno

Estrutura `RetornoGeracaoProcedimento`:

| Campo | Descrição |
|---|---|
| `IdProcedimento` | ID interno do processo no banco |
| `ProcedimentoFormatado` | Número do processo visível para o usuário |
| `LinkAcesso` | Link de acesso ao processo |
| `RetornoInclusaoDocumentos` | Lista de documentos gerados (ver abaixo) |

Cada item de `RetornoInclusaoDocumentos`:

| Campo | Descrição |
|---|---|
| `IdDocumento` | ID interno do documento no banco |
| `DocumentoFormatado` | Número do documento visível para o usuário |
| `LinkAcesso` | Link de acesso ao documento |

---

## Exemplo Completo

```python
import os
import base64
import requests
import urllib3
from dotenv import load_dotenv
from zeep import Client, Settings, xsd
from zeep.transports import Transport

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

wsdl_url         = os.getenv('SEI_WSDL_URL')
sigla_sistema    = os.getenv('SEI_SIGLA_SISTEMA')
chave_acesso     = os.getenv('SEI_CHAVE_ACESSO')
id_unidade_atual = os.getenv('SEI_ID_UNIDADE')

session = requests.Session()
session.verify = False
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})
client = Client(wsdl_url, transport=Transport(session=session), settings=Settings(strict=False))

novo_processo = {
    "IdTipoProcedimento": "100000358",
    "Especificacao": "Teste de Automação",
    "Assuntos": {"items": [{"CodigoEstruturado": "06.10.01.07"}]},
    "Interessados": [{"Sigla": "ATDJ-DIGEPE", "Nome": "Integração Robô API"}],
    "Observacao": "Processo gerado via API SOAP",
    "NivelAcesso": "0",
}

conteudo_html = "<p class=\"Texto_Justificado_Recuo_Primeira_Linha\">Texto do ofício.</p>"
conteudo_b64  = base64.b64encode(conteudo_html.encode("iso-8859-1")).decode("utf-8")

documento_oficio = {
    'Tipo':        'G',
    'IdSerie':     '290',
    'NivelAcesso': '0',
    'Conteudo':    conteudo_b64,
}

resposta = client.service.gerarProcedimento(
    SiglaSistema=sigla_sistema,
    IdentificacaoServico=chave_acesso,
    IdUnidade=id_unidade_atual,
    Procedimento=novo_processo,
    Documentos={'items': [documento_oficio]},
    ProcedimentosRelacionados=xsd.Nil,
    UnidadesEnvio=xsd.Nil,
    SinManterAbertoUnidade='S',
    SinEnviarEmailNotificacao='N',
    DataRetornoProgramado='',
    DiasRetornoProgramado='',
    SinDiasUteisRetornoProgramado='N',
    IdMarcador='',
    TextoMarcador='',
    DataControlePrazo='',
    DiasControlePrazo='',
    SinDiasUteisControlePrazo='N'
)

print(f"Processo: {resposta.ProcedimentoFormatado} | ID: {resposta.IdProcedimento}")
for doc in resposta.RetornoInclusaoDocumentos:
    print(f"  Documento: {doc.DocumentoFormatado} | ID: {doc.IdDocumento}")
```

---

## Observações Gerais

- Para passar parâmetros opcionais do tipo lista como nulos, usar `xsd.Nil` em vez de `None` ou lista vazia — o Zeep valida contra o WSDL e rejeita valores ausentes
- O link retornado em `LinkAcesso` é de **acesso externo** quando a opção "Gerar Links de Acesso Externos" está marcada no cadastro do serviço no SEI — nesse caso o documento precisa estar assinado para ser visualizado pelo link
- Documentos gerados via API podem exibir comportamento de download (`Content-Disposition: attachment`) em ambientes de homologação por configuração do servidor, independente do conteúdo enviado
