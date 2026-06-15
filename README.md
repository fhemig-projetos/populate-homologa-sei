# Populate Homologa Sei

Repositório de testes e investigações da API SOAP do SEI (Sistema Eletrônico de Informações), voltado ao ambiente de homologação da FHEMIG/DIGEPE.

---

## Objetivo

Explorar e documentar o comportamento dos endpoints da API SOAP do SEI v5.0, validando integrações antes de aplicá-las em automações de produção.

---

## Pré-requisitos

- Python 3.10+
- Acesso ao ambiente de homologação do SEI
- Credenciais de sistema cadastradas no SEI (sigla, chave de acesso, ID de unidade)

---

## Instalação

```bash
git clone <url-do-repositorio>
cd populate-homologa-sei
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SEI_WSDL_URL=https://<servidor>/sei/controlador_ws.php?servico=sei
SEI_SIGLA_SISTEMA=<sigla-do-sistema>
SEI_CHAVE_ACESSO=<chave-de-acesso>
SEI_ID_UNIDADE=<id-da-unidade>
```

> O arquivo `.env` não deve ser versionado. Certifique-se de que está no `.gitignore`.

---

## Scripts Disponíveis

| Script | Descrição |
|---|---|
| `gerar_processo.py` | Cria um novo processo no SEI com um documento de ofício gerado internamente |
| `listar_series.py` | Lista os tipos de documento (séries) disponíveis para o serviço |

---

## Documentação dos Endpoints

A pasta [`docs/`](./docs/) contém a documentação detalhada de cada endpoint testado:

| Arquivo | Endpoint | Descrição |
|---|---|---|
| [gerar_procedimento.md](./docs/gerar_procedimento.md) | `gerarProcedimento` | Cria processo com documentos |
| [consultar_procedimento.md](./docs/consultar_procedimento.md) | `consultarProcedimento` | Consulta dados de um processo |
| [consultar_documento.md](./docs/consultar_documento.md) | `consultarDocumento` | Consulta dados de um documento |
| [listar_series.md](./docs/listar_series.md) | `listarSeries` | Lista tipos de documento disponíveis |

---

## Dependências Principais

| Pacote | Uso |
|---|---|
| `zeep` | Cliente SOAP para consumo da API do SEI |
| `requests` | Sessão HTTP customizada (contorno de firewall/SSL) |
| `python-dotenv` | Carregamento de variáveis de ambiente |
| `urllib3` | Supressão de avisos SSL |

---

## Observações Importantes

### Contorno de Firewall
O ambiente de homologação exige que as requisições simulem um User-Agent de navegador. O cliente é configurado com uma sessão `requests` customizada para isso.

### Validação do Zeep
O Zeep valida os parâmetros contra o WSDL antes de enviar a requisição. Para parâmetros opcionais do tipo lista ou string que o WSDL marca como obrigatórios, usar `xsd.Nil` em vez de `None`.

### Links de Acesso Externo
Quando a opção "Gerar Links de Acesso Externos" está ativa no cadastro do serviço no SEI, os links retornados pela API apontam para acesso externo — documentos precisam estar assinados para serem visualizados por esses links.

### Comportamento de Download no Homologação
Documentos gerados via API no ambiente de homologação são servidos com `Content-Disposition: attachment` pelo servidor, causando download ao invés de renderização no visualizador do SEI. Isso é uma configuração do servidor de homologação e **não indica erro no código ou no conteúdo do documento**. O comportamento esperado pode ser verificado pelo link de acesso externo após assinatura do documento.

---

## Referência

- [Documentação oficial SEI Web Services v5.0](./SEI-WebServices-v5_0.pdf)
