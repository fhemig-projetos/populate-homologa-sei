# Estrutura de Dados: Procedimento

Estrutura utilizada para criação de processos no endpoint `gerarProcedimento`.

---

## Campos

| Campo | Tipo | Obrigatoriedade | Descrição |
|---|---|---|---|
| `IdTipoProcedimento` | string | Obrigatório | ID do tipo de processo no SEI. Recomenda-se armazenar em tabela de parâmetros do sistema cliente |
| `NumeroProtocolo` | string | Opcional | Número do processo. Se não informado, o SEI gera automaticamente |
| `DataAutuacao` | string | Opcional | Data de autuação no formato `dd/mm/aaaa`. Se não informada, o SEI usa a data atual |
| `Especificacao` | string | Obrigatório | Especificação/descrição do processo |
| `IdTipoPrioridade` | string | Opcional | ID do tipo de prioridade do processo |
| `Assuntos` | lista | Condicional | Assuntos do processo (ver estrutura `Assunto`). **Obrigatório** ao menos um se o tipo de processo não tiver assuntos sugeridos cadastrados no SEI |
| `Interessados` | lista | Opcional | Conjunto de interessados do processo (ver estrutura `Interessado`). Passar lista vazia se não houver |
| `Observacao` | string | Opcional | Texto de observação da unidade. Passar `null` se não houver |
| `NivelAcesso` | string | Opcional | `0` = público / `1` = restrito / `2` = sigiloso / `null` = herda o nível sugerido para o tipo de processo |
| `IdHipoteseLegal` | string | Condicional | ID da hipótese legal associada. Obrigatório quando `NivelAcesso` for `1` ou `2` |

---

## Estrutura Assunto

| Campo | Descrição |
|---|---|
| `CodigoEstruturado` | Código do assunto no formato `00.00.00.00`, ex: `06.10.01.07` |
| `Descricao` | Descrição do assunto (opcional, informativo) |

---

## Estrutura Interessado

O SEI tenta identificar o contato na seguinte ordem de prioridade:

1. `IdContato`
2. `Cpf`
3. `Cnpj`
4. `Sigla` + `Nome`
5. `Sigla`
6. `Nome`

Se o contato não for encontrado, ele será **cadastrado automaticamente** com os dados fornecidos. Por isso, é recomendável sempre informar o `Nome`.

| Campo | Descrição |
|---|---|
| `IdContato` | ID interno do contato no SEI |
| `Sigla` | Sigla do contato |
| `Nome` | Nome do contato |
| `Cpf` | CPF do contato |
| `Cnpj` | CNPJ do contato |

---

## Exemplo Completo

```python
novo_processo = {
    "IdTipoProcedimento": "100000358",
    "Especificacao": "Descrição detalhada do processo",
    "Assuntos": {
        "items": [
            {"CodigoEstruturado": "06.10.01.07"}
        ]
    },
    "Interessados": [
        {"Sigla": "ATDJ-DIGEPE", "Nome": "Integração Robô API"}
    ],
    "Observacao": "Observação da unidade sobre o processo",
    "NivelAcesso": "0",
}
```

---

## Exemplo com Múltiplos Assuntos e Interessados

```python
novo_processo = {
    "IdTipoProcedimento": "100000358",
    "Especificacao": "Processo com múltiplos assuntos e interessados",
    "Assuntos": {
        "items": [
            {"CodigoEstruturado": "06.10.01.07"},
            {"CodigoEstruturado": "06.10.01.08"},
        ]
    },
    "Interessados": [
        {"Sigla": "SIGLA1", "Nome": "Primeiro Interessado"},
        {"Cpf": "000.000.000-00", "Nome": "Segundo Interessado"},
        {"Cnpj": "00.000.000/0001-00", "Nome": "Empresa Interessada"},
        {"IdContato": "100280566"},
    ],
    "Observacao": None,
    "NivelAcesso": "0",
}
```

---

## Exemplo com Nível de Acesso Restrito

```python
novo_processo = {
    "IdTipoProcedimento": "100000358",
    "Especificacao": "Processo restrito",
    "Assuntos": {"items": [{"CodigoEstruturado": "06.10.01.07"}]},
    "Interessados": [],
    "Observacao": None,
    "NivelAcesso": "1",           # restrito
    "IdHipoteseLegal": "123",     # obrigatório quando NivelAcesso = 1 ou 2
}
```

---

## Observações

- Os assuntos informados são **adicionados** aos assuntos já sugeridos para o tipo de processo no SEI — não os substituem
- Se o tipo de processo não tiver assuntos sugeridos cadastrados, é obrigatório informar pelo menos um em `Assuntos`
- Passar lista vazia em `Interessados` (`[]`) quando não houver interessados — não passar `null`
- O campo `NivelAcesso` como `null` faz o processo herdar o nível sugerido para o tipo de processo conforme cadastro no SEI
