# consultarProcedimento

Retorna informações detalhadas de um processo a partir do seu número visível.

---

## Parâmetros de Entrada

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `SiglaSistema` | string | Sigla do sistema cadastrado no SEI |
| `IdentificacaoServico` | string | Chave de acesso do serviço |
| `IdUnidade` | string | ID da unidade |
| `ProtocoloProcedimento` | string | Número do processo visível para o usuário, ex: `2270.01.0000041/2026-67` |
| `SinRetornarAssuntos` | S/N | Retornar assuntos do processo |
| `SinRetornarInteressados` | S/N | Retornar interessados do processo |
| `SinRetornarObservacoes` | S/N | Retornar observações das unidades |
| `SinRetornarAndamentoGeracao` | S/N | Retornar andamento de geração |
| `SinRetornarAndamentoConclusao` | S/N | Retornar andamento de conclusão |
| `SinRetornarUltimoAndamento` | S/N | Retornar último andamento |
| `SinRetornarUnidadesProcedimentoAberto` | S/N | Retornar unidades onde o processo está aberto |
| `SinRetornarProcedimentosRelacionados` | S/N | Retornar processos relacionados |
| `SinRetornarProcedimentosAnexados` | S/N | Retornar processos anexados |

> Cada sinalizador `S` implica processamento adicional no servidor. Recomenda-se usar `N` para os campos não necessários.

---

## Retorno

Estrutura `RetornoConsultaProcedimento`:

| Campo | Descrição |
|---|---|
| `IdProcedimento` | ID interno do processo |
| `ProcedimentoFormatado` | Número do processo visível para o usuário |
| `Especificacao` | Especificação do processo |
| `DataAutuacao` | Data de autuação |
| `NivelAcessoLocal` | Nível de acesso do processo (0=público, 1=restrito, 2=sigiloso) |
| `NivelAcessoGlobal` | Nível de acesso geral aplicado |
| `LinkAcesso` | Link para acesso ao processo |
| `TipoProcedimento` | Dados do tipo do processo |
| `TipoPrioridade` | Dados do tipo de prioridade |
| `AndamentoGeracao` | Andamento de geração (se `SinRetornarAndamentoGeracao=S`) |
| `AndamentoConclusao` | Andamento de conclusão (se `SinRetornarAndamentoConclusao=S`) |
| `UltimoAndamento` | Último andamento (se `SinRetornarUltimoAndamento=S`) |
| `UnidadesProcedimentoAberto` | Unidades onde está aberto (se `SinRetornarUnidadesProcedimentoAberto=S`) |
| `Assuntos` | Assuntos do processo (se `SinRetornarAssuntos=S`) |
| `Interessados` | Interessados (se `SinRetornarInteressados=S`) |
| `Observacoes` | Observações das unidades (se `SinRetornarObservacoes=S`) |
| `ProcedimentosRelacionados` | Processos relacionados (se `SinRetornarProcedimentosRelacionados=S`) |
| `ProcedimentosAnexados` | Processos anexados (se `SinRetornarProcedimentosAnexados=S`) |

---

## Exemplo Completo

```python
proc_info = client.service.consultarProcedimento(
    SiglaSistema=sigla_sistema,
    IdentificacaoServico=chave_acesso,
    IdUnidade=id_unidade_atual,
    ProtocoloProcedimento='2270.01.0000041/2026-67',
    SinRetornarAssuntos='N',
    SinRetornarInteressados='N',
    SinRetornarObservacoes='N',
    SinRetornarAndamentoGeracao='N',
    SinRetornarAndamentoConclusao='N',
    SinRetornarUltimoAndamento='N',
    SinRetornarUnidadesProcedimentoAberto='N',
    SinRetornarProcedimentosRelacionados='N',
    SinRetornarProcedimentosAnexados='N',
)

print(f"ID Processo:   {proc_info.IdProcedimento}")
print(f"Processo:      {proc_info.ProcedimentoFormatado}")
print(f"Especificacao: {proc_info.Especificacao}")
print(f"Link Acesso:   {proc_info.LinkAcesso}")
```

---

## Observações

- Processos sigilosos não são retornados
- O `LinkAcesso` retornado é de **acesso externo** quando a opção "Gerar Links de Acesso Externos" está marcada no cadastro do serviço no SEI
