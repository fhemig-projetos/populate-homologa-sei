# Automação e Carga de Processos - SEI (API SOAP)

Script em Python desenvolvido para automatizar a criação de processos e geração de documentos no Sistema Eletrônico de Informações (SEI), utilizando a API nativa SOAP. 

Este projeto foi desenhado primariamente para o ambiente de Homologação (ex: Prodemge), servindo para testes de carga, réplica de massa de dados e integração sistêmica.

## Funcionalidades
* Criação automatizada de Processos (Procedimentos) com classificação arquivística (Assuntos) e Interessados vinculados.
* Geração nativa de documentos internos (ex: Ofícios, Despachos) atrelados ao processo via injeção HTML convertida em Base64.
* Bypass automático de WAF (Web Application Firewall) em ambientes governamentais.
* Estrutura blindada via `python-dotenv` para não expor credenciais no repositório.

---

## Tecnologias e Dependências
* **Python 3.x**
* [Zeep](https://docs.python-zeep.org/en/master/) (Cliente SOAP)
* [Requests](https://requests.readthedocs.io/) (Manipulação de sessão e certificados)
* [Python-dotenv](https://saurabh-kumar.com/python-dotenv/) (Gerenciamento de variáveis de ambiente)

---

## Instalação e Configuração

**1. Clone o repositório e acesse a pasta**
```bash
git clone [https://github.com/seu-usuario/populate-homologa-sei.git](https://github.com/seu-usuario/populate-homologa-sei.git)
cd populate-homologa-sei
```

**2. Crie e ative um Ambiente Virtual (Recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
# venv\Scripts\activate   # No Windows
```

**3. Instale as dependências**
```bash
pip install zeep requests python-dotenv
```

**4. Configuração do Cofre de Senhas (.env)**
Crie um arquivo chamado `.env` na raiz do projeto (certifique-se de que ele não será comitado) utilizando o `.env.example` como base:

```env
SEI_WSDL_URL=[https://homologasei.prodemge.gov.br/sei/controlador_ws.php?servico=sei](https://homologasei.prodemge.gov.br/sei/controlador_ws.php?servico=sei)
SEI_SIGLA_SISTEMA=ATDJ-DIGEPE
SEI_CHAVE_ACESSO=sua_chave_secreta_aqui
SEI_ID_UNIDADE=110001324
```

---

## Como Executar

Com o `.env` configurado e o ambiente virtual ativado, basta rodar:

```bash
python gerar_processo.py
```

O terminal retornará o Número de Protocolo visual, o ID interno no banco de dados e o Link público de acesso.

---

## Notas de Engenharia (As Trincheiras do SOAP)

A integração entre linguagens rigorosas como o Python (`zeep`) e sistemas legados como o SEI apresenta desafios de validação de WSDL. Este script utiliza alguns "hacks" arquiteturais fundamentais:

### 1. Desligamento do Strict Mode
A regra do WSDL do SEI e a documentação oficial divergem (o manual pede para mandar vazio, mas o WSDL dita `minOccurs="1"`). Para não ter a requisição bloqueada antes do envio, a validação rigorosa do Zeep foi desativada:
```python
settings = Settings(strict=False)
```

### 2. A Estrutura de Arrays (`{'items': []}`)
Sempre que for mapear uma lista do SEI (como `Assuntos`, `Interessados` ou `Documentos`), é obrigatório utilizar a sintaxe interna de desempacotamento do Zeep (`ArrayValue`), envelopando os dicionários na chave `'items'`:
```python
'Assuntos': {
    'items': [
        {'CodigoEstruturado': '021.1'}
    ]
}
```

### 3. A Bala de Prata do `xsd.Nil`
Não mande listas vazias (`[]`) ou strings vazias (`""`) em campos do tipo Array do SEI que você deseja ignorar (como `ProcedimentosRelacionados`). Para declarar intencionalmente que a chave está vazia sem quebrar o Schema, importe `xsd` do Zeep e passe `xsd.Nil`.

### 4. Renderização de Documentos Internos (Tipo 'G')
Ao enviar textos via API para documentos gerados internamente, passe **apenas as tags HTML essenciais** (ex: `<p>texto</p>`). Não inclua a estrutura raiz (`<html><body>`), pois o SEI já injeta o texto dentro de um template nativo. Formatações excessivas fazem o visualizador colapsar e forçar o download em vez de renderizar na tela.# populate-homologa-sei
