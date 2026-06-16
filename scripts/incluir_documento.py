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

conteudo_html = "<p class=\"Texto_Justificado_Recuo_Primeira_Linha\">Hello World</p>"
conteudo_b64 = base64.b64encode(conteudo_html.encode()).decode()

# A estrutura blindada baseada nos seus scripts de referência
documento_ficticio = {
    'Tipo': 'G',
    'ProtocoloProcedimento': "2270.01.0000050/2026-18",
    'IdSerie': '313',
    'NivelAcesso': '0',   
    'Conteudo': conteudo_b64,
}

resp = client.service.incluirDocumento(        
        SiglaSistema=sigla_sistema,
        IdentificacaoServico=chave_acesso,
        IdUnidade=id_unidade_atual,
        Documento=documento_ficticio
)

print(f"  Documento: {resp.DocumentoFormatado}")
print(f"  ID Doc: {resp.IdDocumento}")
print(f"  Link Doc: {resp.LinkAcesso}")


