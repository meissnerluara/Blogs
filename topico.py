# Importando a Função de Conexão com o Banco de Dados
from conexao import conectar

# Dicionário
topicos = {}
# chave: id_topico
# {"nome" : "valor_nome", "descricao" : "valor_descricao"}

# Função para carregar os tópicos do banco de dados para o dicionário
def carregar_topicos():
    global topicos
    topicos.clear()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM topicos")
    for (id_topico, nome, descricao) in cursor:
        topicos[str(id_topico)] = {
            "nome": nome,
            "descricao": descricao
        }
    cursor.close()
    conexao.close()

# Função para criar um novo tópico
def criar():
    nome = input("Nome: ")
    descricao = input("Descrição: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO topicos (nome, descricao) VALUES (%s, %s)", (nome, descricao))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_topicos()
    print(f"\nTópico {nome} incluído com sucesso!")

# Função para visualizar os tópicos cadastrados
def visualizar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_topico, nome, descricao FROM topicos")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    if resultados:
        for linha in resultados:
            print(f" {linha[0]} | {linha[1]} | {linha[2]}")
    else:
        print("\nNenhum tópico encontrado.")

# Função para excluir um tópico pelo ID
def excluir():
    id_topico = input("Id do Tópico: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM topicos WHERE id_topico = %s", (id_topico,))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_topicos()
    print("\nTópico excluído com sucesso!")

# Função para editar um tópico existente
def editar():
    id_topico = input("Id do Tópico: ")
    nome = input("Novo nome: ")
    descricao = input("Nova descrição: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE topicos SET nome=%s, descricao=%s WHERE id_topico=%s",
                   (nome, descricao, id_topico))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_topicos()
    print(f"\nTópico {nome} atualizado com sucesso!")
