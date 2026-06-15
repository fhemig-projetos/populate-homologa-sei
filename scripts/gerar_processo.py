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
            
# Estrutura do Processo
novo_processo = {
    "IdTipoProcedimento": "100000358",
    "Especificacao": "Teste de Carga e Automação - Réplica de Processo Produtivo",
    "Assuntos": {"items": [{"CodigoEstruturado": "06.10.01.07"}]},
    "Interessados": [
            {"Sigla": "ATDJ-DIGEPE", "Nome": "Integração Robô API"}
        ],    
    "Observacao": "Processo populado via script Python utilizando API SOAP",
    "NivelAcesso": "0",
}

conteudo_html = "<p class=\"Texto_Justificado_Recuo_Primeira_Linha\">Hello World</p>"
conteudo_b64 = base64.b64encode(conteudo_html.encode("iso-8859-1")).decode("utf-8")

# A estrutura blindada baseada nos seus scripts de referência
documento_ficticio = {
    'Tipo': 'G',
    'IdSerie': '313',
    'NivelAcesso': '0',   
    'Conteudo': conteudo_b64,
}

# Execução
try:
    resposta = client.service.gerarProcedimento(
        SiglaSistema=sigla_sistema,
        IdentificacaoServico=chave_acesso,
        IdUnidade=id_unidade_atual,
        Procedimento=novo_processo,
        Documentos={'items': [documento_ficticio]},
        ProcedimentosRelacionados=xsd.Nil,   
        UnidadesEnvio=xsd.Nil,               
        SinManterAbertoUnidade='S',       
        SinEnviarEmailNotificacao='N',     
        DataRetornoProgramado='',
        DiasRetornoProgramado='',
        SinDiasUteisRetornoProgramado='N', 
        IdMarcador='',
        TextoMarcador='',
        DataControlePrazo='',             
        DiasControlePrazo='',             
        SinDiasUteisControlePrazo='N'     
    )
    
    print("Processo criado com sucesso!")
    print(f"Número Formatado (Visual): {resposta.ProcedimentoFormatado}")
    print(f"ID Interno do Processo (Banco): {resposta.IdProcedimento}")
    print(f"Link Público de Consulta Externa: {resposta.LinkAcesso}")

    for doc in resposta.RetornoInclusaoDocumentos:
        print(f"  Documento: {doc.DocumentoFormatado}")
        print(f"  ID Doc: {doc.IdDocumento}")
        print(f"  Link Doc: {doc.LinkAcesso}")

except Exception as e:
    print(f"Erro na integração SOAP: {e}")
