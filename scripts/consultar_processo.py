import os
import requests
import urllib3
from dotenv import load_dotenv
from zeep import Client, Settings, xsd
from zeep.transports import Transport
import base64

# Carrega as variáveis do arquivo .env para a memória do script
load_dotenv()

# Silencia os avisos de proxy/SSL no terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Puxa as variáveis de forma segura do .env
wsdl_url = os.getenv('SEI_WSDL_URL')
sigla_sistema = os.getenv('SEI_SIGLA_SISTEMA')
chave_acesso = os.getenv('SEI_CHAVE_ACESSO')
id_unidade_atual = os.getenv('SEI_ID_UNIDADE')

# Truque para passar pelo Firewall / Disfarce de Navegador
session = requests.Session()
session.verify = False  
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
transport = Transport(session=session)

# Desliga o validador do Zeep
settings = Settings(strict=False)

# Inicializa o cliente SOAP com o disfarce e as configurações
client = Client(wsdl_url, transport=transport, settings=settings)


proc_info = client.service.consultarProcedimento(
    SiglaSistema=sigla_sistema,
    IdentificacaoServico=chave_acesso,
    IdUnidade=id_unidade_atual,
    ProtocoloProcedimento='2270.01.0000041/2026-67',  # o ProcedimentoFormatado
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

print(proc_info.LinkAcesso)
print(proc_info.ProcedimentoFormatado)
print(proc_info.Especificacao)
