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

conteudo_html = """
<h3 style="text-align: center;">Documento de Teste - Integração API</h3>

<p>Prezados,</p>

<p><strong>Lorem ipsum dolor sit amet</strong>, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>

<p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

<p><em>Pontos de atenção verificados neste teste:</em></p>
<ul>
    <li>Renderização nativa no visualizador web do SEI.</li>
    <li>Codificação UTF-8 para garantir que a acentuação (ç, ã, á) não force o download.</li>
    <li>Injeção correta de destinatários no cabeçalho do documento.</li>
</ul>

<p>Atenciosamente,</p>
<p><strong>Robô de Automação (ATDJ-DIGEPE)</strong></p>
"""
conteudo_b64 = base64.b64encode(conteudo_html.encode()).decode()

# A estrutura blindada baseada nos seus scripts de referência
documento_ficticio = {
    'Tipo': 'G',
    'ProtocoloProcedimento': "2270.01.0000003/2026-26",
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


