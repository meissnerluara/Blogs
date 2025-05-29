# Importando a Função de Conexão com o Banco de Dados
from conexao import conectar

# Dicionário
usuarios = {}
# chave: id_usuario
# {"nome" : "valor_nome", "email" : "valor_email", "senha" : "valor_senha"}

# Função para carregar os usuários do banco de dados para o dicionário
def carregar_usuarios():
    global usuarios
    usuarios.clear()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios")
    for (id_usuario, nome, email, senha) in cursor:
        usuarios[str(id_usuario)] = {
            "nome": nome,
            "email": email,
            "senha": senha
        }
    cursor.close()
    conexao.close()

# Função para cadastrar um novo usuário
def cadastar():
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_usuarios()
    print(f"\nUsuário {nome} incluído com sucesso!")

# Função para consultar os usuários cadastrados
def consultar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_usuario, nome, email, senha FROM usuarios")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    if resultados:
        for linha in resultados:
            print(f" {linha[0]} | {linha[1]} | {linha[2]} | {linha[3]}")
    else:
        print("\nNenhum usuário encontrado.")

# Função para excluir um usuário pelo ID
def remover():
    id_usuario = input("Informe o Id do Usuário: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_usuarios()
    print("\nUsuário excluído com sucesso!")

# Função para editar um usuário existente
def atualizar():
    id_usuario = input("Id do Usuário: ")
    nome = input("Novo nome: ")
    email = input("Novo email: ")
    senha = input("Nova senha: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET nome=%s, email=%s, senha=%s WHERE id_usuario=%s",
                   (nome, email, senha, id_usuario))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_usuarios()
    print(f"\nUsuário {nome} atualizado com sucesso!")
