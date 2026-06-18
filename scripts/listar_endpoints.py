import os
import requests
import urllib3
from dotenv import load_dotenv
from zeep import Client, Settings
from zeep.transports import Transport

# 1. Configurações Iniciais Seguras
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

wsdl_url = os.getenv('SEI_WSDL_URL')
sigla_sistema = os.getenv('SEI_SIGLA_SISTEMA')
chave_acesso = os.getenv('SEI_CHAVE_ACESSO')

session = requests.Session()
session.verify = False  
session.headers.update({'User-Agent': 'Mozilla/5.0'})
transport = Transport(session=session)

# Strict=False para não sermos bloqueados pelo próprio Python antes de testar o SEI
settings = Settings(strict=False)
client = Client(wsdl_url, transport=transport, settings=settings)

print("🔍 Iniciando varredura de permissões no SEI...\n")

liberados = []
bloqueados = []

# 2. Pega a lista de todas as funções do WSDL
operacoes = [op.name for service in client.wsdl.services.values() 
                     for port in service.ports.values() 
                     for op in port.binding._operations.values()]

# 3. O Teste de Fogo (Bate na porta de cada uma)
for operacao in operacoes:
    try:
        # Pega a função dinamicamente dentro do client.service
        funcao_api = getattr(client.service, operacao)
        
        # Tenta executar passando APENAS as credenciais
        # O SEI vai barrar isso de alguma forma, o que importa é COMO ele barra.
        funcao_api(SiglaSistema=sigla_sistema, IdentificacaoServico=chave_acesso)
        
    except Exception as e:
        mensagem_erro = str(e)
        
        # Se a mensagem contiver "não liberado" ou "não cadastrado", a porta está trancada.
        if "não liberado" in mensagem_erro.lower() or "não cadastrado" in mensagem_erro.lower():
            bloqueados.append(operacao)
        else:
            # Se deu qualquer outro erro (ex: Missing element, Parâmetro vazio), a porta está aberta!
            liberados.append(operacao)

# 4. Relatório Final
print("✅ ENDPOINTS QUE VOCÊ TEM ACESSO (Liberados):")
for op in sorted(liberados):
    print(f"  - {op}")

print("\n❌ ENDPOINTS BLOQUEADOS (Requer painel do Administrador):")
for op in sorted(bloqueados):
    print(f"  - {op}")