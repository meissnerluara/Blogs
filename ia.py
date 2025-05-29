# Importando as Bibliotecas
import cohere
import os
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave da API da Cohere armazenada no .env
API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(API_KEY)

# Função para gerar um título de postagem baseado no conteúdo fornecido
def gerar_titulo(conteudo):
    mensagem = f"Crie um título criativo e curto para esta postagem: {conteudo}"
    
    resposta = co.chat(
        model="command-r-plus",
        message=mensagem,
        temperature=0.7
    )
    
    titulo = resposta.text.strip()
    return titulo