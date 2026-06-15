# consultarDocumento

Retorna informações detalhadas de um documento a partir do seu número visível.

---

## Parâmetros de Entrada

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `SiglaSistema` | string | Sigla do sistema cadastrado no SEI |
| `IdentificacaoServico` | string | Chave de acesso do serviço |
| `IdUnidade` | string | ID da unidade |
| `ProtocoloDocumento` | string | Número do documento visível para o usuário, ex: `0114651` |
| `SinRetornarAndamentoGeracao` | S/N | Retornar andamento de geração do documento |
| `SinRetornarAssinaturas` | S/N | Retornar assinaturas do documento |
| `SinRetornarPublicacao` | S/N | Retornar dados de publicação |
| `SinRetornarCampos` | S/N | Retornar campos do formulário |
| `SinRetornarBlocos` | S/N | Retornar blocos na unidade que contém o documento |

> Cada sinalizador `S` implica processamento adicional no servidor. Recomenda-se usar `N` para os campos não necessários.

---

## Retorno

Estrutura `RetornoConsultaDocumento`:

| Campo | Descrição |
|---|---|
| `IdProcedimento` | ID interno do processo |
| `ProcedimentoFormatado` | Número do processo visível para o usuário |
| `IdDocumento` | ID interno do documento |
| `DocumentoFormatado` | Número do documento visível para o usuário |
| `NivelAcessoLocal` | Nível de acesso do documento (0=público, 1=restrito, 2=sigiloso) |
| `NivelAcessoGlobal` | Nível de acesso geral do processo |
| `LinkAcesso` | Link para acesso ao documento |
| `Serie` | Dados do tipo do documento |
| `Numero` | Número do documento |
| `Descricao` | Descrição do documento |
| `Data` | Data de geração |
| `UnidadeElaboradora` | Unidade que gerou o documento |
| `AndamentoGeracao` | Andamento de geração (se `SinRetornarAndamentoGeracao=S`) |
| `Assinaturas` | Assinaturas do documento (se `SinRetornarAssinaturas=S`) |
| `Publicacao` | Dados de publicação (se `SinRetornarPublicacao=S`) |
| `Campos` | Campos do formulário (se `SinRetornarCampos=S`) |
| `Blocos` | Blocos na unidade (se `SinRetornarBlocos=S`) |

---

## Exemplo Completo

```python
doc_info = client.service.consultarDocumento(
    SiglaSistema=sigla_sistema,
    IdentificacaoServico=chave_acesso,
    IdUnidade=id_unidade_atual,
    ProtocoloDocumento='0114651',
    SinRetornarAndamentoGeracao='N',
    SinRetornarAssinaturas='N',
    SinRetornarPublicacao='N',
    SinRetornarCampos='N',
    SinRetornarBlocos='N',
)

print(f"ID Documento:  {doc_info.IdDocumento}")
print(f"Documento:     {doc_info.DocumentoFormatado}")
print(f"Processo:      {doc_info.ProcedimentoFormatado}")
print(f"Link Acesso:   {doc_info.LinkAcesso}")
```

---

## Observações

- O `LinkAcesso` retornado é de **acesso externo** quando a opção "Gerar Links de Acesso Externos" está marcada no cadastro do serviço no SEI
- Documentos de processos sigilosos não são retornados
- Para scraping do conteúdo do documento, o `LinkAcesso` externo pode ser utilizado após o documento estar assinado
