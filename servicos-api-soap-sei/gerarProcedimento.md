# Operação Principal: `gerarProcedimento` (API SOAP SEI)
A operação `gerarProcedimento` é o *endpoint* principal para a criação de novos processos no SEI. Ela recebe as credenciais de autenticação, os metadados do processo e, simultaneamente, pode injetar documentos, criar relacionamentos e despachar o processo para outras unidades.

**Atenção Desenvolvedores (Python/Zeep):** A documentação oficial frequentemente instrui o envio de "conjuntos vazios" para parâmetros opcionais. No entanto, o validador interno da biblioteca Zeep bloqueará strings, listas, `None` ou dicionários vazios (`[]`, `""`, `{}`) devido à regra `minOccurs="1"` do WSDL. Siga estritamente as regras de contorno (`xsd.Nil` e `{'items': [...]}`) documentadas abaixo.

---

### Parâmetros de Entrada (Input)

#### 1. Credenciais e Contexto
* **`SiglaSistema` (Obrigatório)**
  * **Tipo:** `String`
  * **Descrição:** Sigla exata cadastrada no painel do SEI (Menu *Administração > Sistemas*). Ex: `'ATDJ-DIGEPE'`.
* **`IdentificacaoServico` (Obrigatório)**
  * **Tipo:** `String`
  * **Descrição:** O *Token* (hash ou chave alfanumérica) gerado pelo administrador do SEI e atrelado ao sistema acima.
* **`IdUnidade` (Obrigatório)**
  * **Tipo:** `String`
  * **Descrição:** Identificador numérico da unidade (PK no banco) em que o processo nascerá. **Atenção:** Não é a sigla em texto (ex: "RH"), mas sim o ID interno (ex: `'110009999'`).

#### 2. Carga de Dados (Payloads Complexos)
* **`Procedimento` (Obrigatório)**
  * **Tipo:** `Objeto (Dicionário)`
  * **Descrição:** Estrutura contendo os metadados do processo (Assuntos, Interessados, Tipo). *Consulte a documentação específica da estrutura `Procedimento`.*
* **`Documentos` (Obrigatório WSDL)**
  * **Tipo:** `Array de Objetos (Documento)`
  * **Descrição:** Lista de documentos a serem criados/anexados no momento zero do processo.
  * **Atenção Zeep (O Cavalo de Troia):** O manual diz "se nenhum, informar conjunto vazio". O Zeep bloqueará. Para evitar erros:
    * Se for enviar: Enclausure na sintaxe `{'items': [ {doc1}, {doc2} ]}`.
    * Se NÃO for enviar: Importe a classe `xsd` do Zeep e passe o valor **`xsd.Nil`**. Isso criará uma tag XML `<Documentos xsi:nil="true"/>` que o SEI aceita perfeitamente.
* **`ProcedimentosRelacionados` (Obrigatório WSDL)**
  * **Tipo:** `Array de Strings` (IDs de outros processos).
  * **Atenção Zeep (A Bala de Prata):** Se você não quiser relacionar nenhum processo, **NÃO** passe `None`, `{}`, `[]` ou `""`. Importe a classe `xsd` do Zeep e passe o valor **`xsd.Nil`**. Isso criará uma tag XML `<ProcedimentosRelacionados xsi:nil="true"/>` que o SEI aceita perfeitamente.
* **`UnidadesEnvio` (Obrigatório WSDL)**
  * **Tipo:** `Array de Strings` (IDs de outras unidades).
  * **Descrição:** Unidades para onde o processo será tramitado automaticamente logo após nascer.
  * **Atenção Zeep:** Mesma regra acima. Se não for tramitar para ninguém agora, passe **`xsd.Nil`**.

#### 3. Flags e Regras de Negócio (Sinalizadores) 
*(Nota: O SEI utiliza 'S' para Sim e 'N' para Não. Todos são strings)*
* **`SinManterAbertoUnidade` (Obrigatório)** 
  * **Tipo:** `String` (Padrão: `'S'`)
  * **Descrição:** Se o processo for despachado para outra unidade (via `UnidadesEnvio`), ele deve continuar aberto na sua unidade de origem?
* **`SinEnviarEmailNotificacao` (Obrigatório)**
  * **Tipo:** `String` (Padrão: `'N'`)
  * **Descrição:** Dispara e-mail padrão do SEI para as unidades de destino avisando da chegada do processo.

#### 4. Prazos e Retornos (Obrigatórios)
*(Dica: Se não for usar controle de prazo, passe sempre String Vazia `''`, nunca passe `None` para evitar quebra do Schema)*
* **`DataRetornoProgramado` / `DataControlePrazo`:** `String` (Formato: DD/MM/AAAA). Passar `''` se não usar.
* **`DiasRetornoProgramado` / `DiasControlePrazo`:** `String` (Numérica). Passar `''` se não usar.
* **`SinDiasUteisRetornoProgramado` / `SinDiasUteisControlePrazo`:** `String` (`'S'` ou `'N'`). Padrão é `'N'`.

#### 5. Marcadores (Obrigatórios)
* **`IdMarcador`:** `String`. ID interno da etiqueta colorida/marcador da unidade. Passar `''` se não usar.
* **`TextoMarcador`:** `String`. Texto visível ao passar o mouse sobre o marcador. Passar `''` se não usar.

---

#### ???Investigar esses parâmetros???
### Parâmetros de Saída (Output)
A chamada retorna um objeto do tipo `RetornoGeracaoProcedimento` que contém as chaves para armazenar no seu banco de dados ou exibir ao usuário:
* **`IdProcedimento`:** O ID interno real (PK) do processo salvo no banco. Útil para futuras chamadas de API (ex: incluir mais documentos depois).
* **`ProcedimentoFormatado`:** A string visual e amigável do processo com a máscara (ex: `12345.000001/2023-99`).
* **`LinkAcesso`:** URL pública/direta para visualização da árvore do processo gerado.

---

### Exemplo de Implementação Limpa (Python/Zeep)

```python
from zeep import xsd

# A estrutura de chamada perfeitamente tipada para o validador WSDL
resposta = client.service.gerarProcedimento(
    SiglaSistema='SIGLA_MEU_SISTEMA',
    IdentificacaoServico='CHAVE_ALFANUMERICA',
    IdUnidade='ID_UNIDADE',
    Procedimento=novo_processo_dict, # Ver estrutura mapeada correspondente
    
    # Lidando com Payloads Complexos
    Documentos={'items': [meu_documento_ficticio]}, # ou xsd.Nil
    ProcedimentosRelacionados=xsd.Nil,  
    UnidadesEnvio=xsd.Nil,              
    
    # Flags Booleanas (S/N)
    SinManterAbertoUnidade='S',       
    SinEnviarEmailNotificacao='N',     
    
    # Preenchimento vazio (Blank) para evitar quebra de Schema
    DataRetornoProgramado='',
    DiasRetornoProgramado='',
    SinDiasUteisRetornoProgramado='N', 
    IdMarcador='',
    TextoMarcador='',
    DataControlePrazo='',             
    DiasControlePrazo='',             
    SinDiasUteisControlePrazo='N'     
)