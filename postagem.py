# Importando as Funções de Conexão com o Banco de Dados e de Geração de Título com IA
from conexao import conectar
from ia import gerar_titulo

# Dicionário
postagens = {}
# chave: id_postagem
# {"titulo" : "valor_titulo", "conteudo" : "valor_conteudo", "data_publicacao" : "valor_data_publicacao", "id_usuario" : "valor_id_usuario", "id_topico" : "valor_id_topico"}

# Função para carregar as postagens do banco de dados para o dicionário
def carregar_postagens():
    global postagens
    postagens.clear()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM postagens")
    for (id_postagem, titulo, conteudo, data_publicacao, id_usuario, id_topico) in cursor:
        postagens[str(id_postagem)] = {
            "titulo": titulo,
            "conteudo": conteudo,
            "data_publicacao": data_publicacao,
            "id_usuario": str(id_usuario),
            "id_topico": str(id_topico)
        }
    cursor.close()
    conexao.close()

# Função para criar uma nova postagem
def criar():
    usar_ia = input("Deseja gerar o título com IA? (s/n): ").lower()

    if usar_ia == 's':
        conteudo = input("\nDigite o conteúdo da postagem: ")
        titulo = gerar_titulo(conteudo)
        print(f"\nTítulo sugerido pela IA: {titulo}")
    else:
        titulo = input("\nTítulo: ")
        conteudo = input("Conteúdo: ")

    id_usuario = input("\nId do Usuário: ")
    id_topico = input("Id do Tópico: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO postagens (titulo, conteudo, id_usuario, id_topico) VALUES (%s, %s, %s, %s)",
                   (titulo, conteudo, id_usuario, id_topico))
    conexao.commit()
    cursor.close()
    conexao.close()

    carregar_postagens()
    print(f"\nPostagem '{titulo}' criada com sucesso!")

# Função para visualizar as postagens cadastradas
def visualizar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_postagem, titulo, conteudo, data_publicacao, id_usuario, id_topico senha FROM postagens")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    if resultados:
        for linha in resultados:
            print(f" {linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]}")
    else:
        print("\nNenhuma postagem encontrada.")