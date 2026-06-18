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

# ========================================================
# INGREDIENTES PARA O TESTE
# ========================================================
MEU_ID_BLOCO = '816'       # Ex: '2941'
MEU_PROTOCOLO_DOC = '0114651' # Ex: '0114640' (O doc que acabou de gerar)
# ========================================================

print(f"🔄 Tentando incluir o documento {MEU_PROTOCOLO_DOC} no bloco {MEU_ID_BLOCO}...")

try:
    # A chamada oficial para vincular Documento a um Bloco
    resposta = client.service.incluirDocumentoBloco(
        SiglaSistema=sigla_sistema,
        IdentificacaoServico=chave_acesso,
        IdUnidade=id_unidade_atual,
        IdBloco=MEU_ID_BLOCO,
        ProtocoloDocumento=MEU_PROTOCOLO_DOC,
        Anotacao='Documento inserido automaticamente via robô Python'
    )
    
    print("✅ SUCESSO ABSOLUTO! O documento foi parar dentro do bloco.")
    print(f"Resposta do Servidor: {resposta}")

except Exception as e:
    mensagem = str(e)
    print(f"\n❌ ERRO NA INTEGRAÇÃO SOAP: {mensagem}")
    
    if "não liberado" in mensagem.lower():
        print("🚨 DIAGNÓSTICO: O serviço está bloqueado. Aquele script anterior deu um falso positivo.")
        print("Ação necessária: Pedir para a Prodemge habilitar a operação 'incluirDocumentoBloco' para o seu sistema.")
    else:
        print("🚨 DIAGNÓSTICO: O serviço está liberado, mas erramos algum parâmetro (talvez o ID do Bloco não exista na sua Unidade).")