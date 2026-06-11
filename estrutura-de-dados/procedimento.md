# Estrutura de Dados: `Procedimento` (API SOAP SEI)

A estrutura `Procedimento` é o payload principal utilizado na operação `gerarProcedimento`. Ela dita as regras de negócio e os metadados para a abertura de um novo processo no SEI.

**Atenção Desenvolvedores (Python/Zeep):** O WSDL do SEI possui regras de validação rigorosas (`minOccurs="1"`) que frequentemente entram em conflito com a documentação oficial (que sugere o envio de strings, listas, dicionários vazios ou `None`). Siga as diretrizes de "Tipos" abaixo para evitar bloqueios estruturais antes mesmo da requisição atingir o servidor.

---

### Dicionário de Campos

#### `IdTipoProcedimento` (Obrigatório)
* **Tipo:** `String`
* **Descrição:** Identificador interno (Primary Key no banco de dados do SEI) correspondente ao tipo de processo que será aberto. 
* **Dica Prática:** Não é o código visível nem a nomenclatura (ex: "Administração: Geral"). Em ambientes de teste, pode ser pescado inspecionando o elemento por meio do `Chrome Dev Tools` (ou similar) no momento de escolha do tipo de processo, durante a criação do Processo SEI. Em produção, deve ser obtido via extração "De-Para" com os administradores do banco de dados.

#### `NumeroProtocolo` (Opcional)
* **Tipo:** `String`
* **Descrição:** Número visível do processo (ex: `12345.00001/2023-11`). 
* **Uso:** Apenas se o seu sistema legiferar a numeração. Omitir ou passar nulo/string vazia para que o próprio SEI gere a numeração padrão (Recomendado).

#### `DataAutuacao` (Opcional)
* **Tipo:** `String` (Formato: `DD/MM/AAAA`)
* **Descrição:** Data retroativa de criação do processo. 
* **Uso:** Omitir ou passar vazio para utilizar o *timestamp* atual do servidor.

#### `Especificacao` (Obrigatório na prática)
* **Tipo:** `String` (Limite: Geralmente 50 caracteres)
* **Descrição:** Resumo ou título descritivo do processo que aparecerá na árvore e nas pesquisas.

#### `IdTipoPrioridade` (Opcional)
* **Tipo:** `String`
* **Descrição:** Identificador do banco de dados para a prioridade (ex: Tramitação Prioritária, Estatuto do Idoso). Omitir caso a tramitação seja normal.

#### `Assuntos` (Obrigatório na prática)
* **Tipo:** `Array de Objetos (Assunto)`
* **Descrição:** Lista de dicionários contendo a classificação arquivística (CONARQ). 
* **Atenção Zeep:** Se o tipo do processo não possuir assuntos pré-cadastrados, a API barrará a requisição se estiver vazio. 
* **Exemplo de uso genérico:** 
```
'Assuntos': {
        'items': [
            {'CodigoEstruturado': '021.1'},   # Primeiro assunto
            {'CodigoEstruturado': '000.11'},  # Segundo assunto
            {'CodigoEstruturado': '900.01'}   # Terceiro assunto (e assim por diante...)
        ]
    },
```
- Ou passar `xsd.nil` para forçar conjunto vazio.
> **ATENÇÃO!** Caso passe algum valor, você deverá substituir o código por um código real!!! 

#### `Interessados` (Opcional)
* **Tipo:** `Array de Objetos (Interessado)`
* **Descrição:** Lista de CPFs, CNPJs ou Nomes vinculados ao processo. A API busca atrelar a contatos existentes ou criar novos automaticamente.
* **Atenção Zeep (O Cavalo de Troia):** A documentação oficial diz "informar conjunto vazio se não existirem". Porém, o WSDL exige `minOccurs="1"`. Enviar uma lista, string, `None` ou dicionário vazio (`[]`, `""`, `{}`) em Python quebra a biblioteca local.
* **Solução:** 
Importar `xsd` e passar `xsd.Nil` para forçar esse conjunto vazio ou envie sempre pelo menos um interessado. Caso não exista um real, envie um registro *dummy* com os dados da própria unidade integradora: 
  `[{'Sigla': 'SUA-SIGLA', 'Nome': 'Integração via API'}]`.

#### `Observacao` (Opcional)
* **Tipo:** `String`
* **Descrição:** Anotações adicionais da unidade. Aparece no ícone de "informação" ao lado do processo na interface. Passar string vazia `""` ou omitir se não houver.

#### `NivelAcesso` (Obrigatório)
* **Tipo:** `String` (Valores: `'0'`, `'1'`, `'2'`)
* **Descrição:** Define a visibilidade do processo.
  * `'0'` - Público
  * `'1'` - Restrito
  * `'2'` - Sigiloso

#### `IdHipoteseLegal` (Condicional)
* **Tipo:** `String`
* **Descrição:** ID interno do embasamento legal. 
* **Regra:** Estritamente obrigatório caso o `NivelAcesso` seja `'1'` (Restrito) ou `'2'` (Sigiloso).

---

### Exemplo de Implementação Limpa (Python/Zeep)

Para evitar erros de esquema (`Missing element` ou `minOccurs check`) devido a campos vazios, a estrutura deve ser montada contendo apenas o essencial, deixando que o WSDL assuma os valores default para campos não declarados:

```python
novo_processo = {
    'IdTipoProcedimento': '100048996',
    'Especificacao': 'Processo gerado via automação API SOAP',
    'Assuntos': {"items": [{"CodigoEstruturado": "06.10.01.07"}]},
    'Interessados': [
        {'Sigla': 'SETOR-TI', 'Nome': 'Robô de Integração'}
    ],
    'Observacao': 'Processo populado via script Python utilizando API SOAP',
    'NivelAcesso': '0'
}