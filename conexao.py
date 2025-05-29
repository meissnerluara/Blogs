# Importando as Bibliotecas
import mysql.connector
from dotenv import load_dotenv
import os

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para conexão com o banco de dados
def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
