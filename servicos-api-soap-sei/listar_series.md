# listarSeries

Lista os tipos de documento (séries) disponíveis para o serviço configurado no SEI.

---

## Parâmetros de Entrada

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `SiglaSistema` | string | Sigla do sistema cadastrado no SEI |
| `IdentificacaoServico` | string | Chave de acesso do serviço |
| `IdUnidade` | string | ID da unidade (opcional como filtro adicional) |
| `IdTipoProcedimento` | string/Nil | Filtra séries pelo tipo de processo (opcional) |

> O WSDL desta instalação exige que `IdTipoProcedimento` seja passado explicitamente como `xsd.Nil` quando não utilizado — passá-lo ausente causa `ValidationError` no Zeep.

---

## Retorno

Lista de estruturas `Serie`:

| Campo | Descrição |
|---|---|
| `IdSerie` | Identificador interno do tipo de documento |
| `Nome` | Nome do tipo de documento |
| `Aplicabilidade` | `T` = interno e externo / `I` = somente interno / `E` = somente externo / `F` = formulário |

---

## Exemplo Completo

```python
from zeep import xsd

series = client.service.listarSeries(
    SiglaSistema=sigla_sistema,
    IdentificacaoServico=chave_acesso,
    IdUnidade=id_unidade_atual,
    IdTipoProcedimento=xsd.Nil,
)

for s in series:
    print(s.IdSerie, s.Nome, s.Aplicabilidade)
```

---

## Observações

- As séries retornadas são filtradas pelo acesso configurado para o serviço no SEI — apenas os tipos de documento liberados nas operações do serviço aparecem
- A aplicabilidade `I` indica que o tipo de documento só pode ser gerado internamente (`Tipo='G'`) — não aceita documentos externos (`Tipo='R'`)
- A aplicabilidade `E` indica o contrário: só aceita documentos externos
- O parâmetro `IdSerie` **não existe** no WSDL desta instalação, ao contrário do que a documentação oficial v5.0 descreve — usar apenas `IdTipoProcedimento` como filtro opcional

---

## IDs de Séries Relevantes Mapeados

| IdSerie | Nome | Aplicabilidade |
|---|---|---|
| 290 | Ofício | T |
| 291 | Despacho | T |
| 292 | Ofício-Circular | T |
| 293 | Anexo | T |
| 313 | Memorando | T |
| 296 | Comunicado | T |
| 300 | Nota Técnica | T |
| 348 | Relatório | T |
| 371 | Ata | T |
| 452 | Parecer | T |
