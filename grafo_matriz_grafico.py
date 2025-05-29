# Importando as Bibliotecas
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import usuario
import topico
import postagem

# Matriz de Postagens (Usuário x Tópico)
def visualizar_matriz():
    # Carregando dados de usuários, tópicos e postagens
    usuario.carregar_usuarios()
    topico.carregar_topicos()
    postagem.carregar_postagens()
    usuarios = usuario.usuarios
    topicos = topico.topicos
    postagens = postagem.postagens

    # Criando a matriz
    matriz = np.zeros((len(usuarios), len(topicos)), dtype=int)

    # Preenchendo a matriz
    for i, uid in enumerate(usuarios):
        for j, tid in enumerate(topicos):
            count = 0
            for pid in postagens:
                if (postagens[pid]['id_usuario'] == uid and 
                    postagens[pid]['id_topico'] == tid):
                    count += 1
            matriz[i][j] = count

    # Exibindo a matriz no console
    print("Matriz de Postagens (Usuário x Tópico):")
    print("          " + "  ".join(f"{topicos[tid]['nome']:>6}" for tid in topicos))
    for i, uid in enumerate(usuarios):
        linha = "  ".join(f"{matriz[i][j]:6}" for j in range(len(topicos)))
        print(f"{usuarios[uid]['nome']:<10} {linha}")

# Grafo de Conexões entre Usuário x Tópico
def visualizar_grafo():
    # Carregando dados de usuários, tópicos e postagens
    usuario.carregar_usuarios()
    topico.carregar_topicos()
    postagem.carregar_postagens()
    usuarios = usuario.usuarios
    topicos = topico.topicos
    postagens = postagem.postagens

    # Criando o grafo
    B = nx.Graph()

    # Lista com os nomes dos usuários e tópicos
    user_nodes = [usuarios[uid]['nome'] for uid in usuarios]
    topic_nodes = [topicos[tid]['nome'] for tid in topicos]

    # Adicionando nós de usuários e tópicos
    B.add_nodes_from(user_nodes, bipartite=0)
    B.add_nodes_from(topic_nodes, bipartite=1)

    # Adicionando arestas conectando os usuários aos tópicos
    for pid in postagens:
        user = usuarios[postagens[pid]['id_usuario']]['nome']
        topic = topicos[postagens[pid]['id_topico']]['nome']
        B.add_edge(user, topic)

    # Definindo a posição dos nós
    pos = dict()
    pos.update((node, (1, i)) for i, node in enumerate(user_nodes))
    pos.update((node, (2, i)) for i, node in enumerate(topic_nodes))

    # Desenhando o grafo
    plt.figure(figsize=(10, 6))
    nx.draw(B, pos, with_labels=True, node_color=['lightblue' if node in user_nodes else 'lightgreen' for node in B.nodes()],
            edge_color='gray', node_size=1000, font_size=9)
    plt.title("Usuários x Tópicos")
    plt.show()

# Gráfico de Barras (Usuário x Tópico)
def visualizar_grafico():
    # Carregando dados de usuários, tópicos e postagens
    usuario.carregar_usuarios()
    topico.carregar_topicos()
    postagem.carregar_postagens()
    usuarios = usuario.usuarios
    topicos = topico.topicos
    postagens = postagem.postagens

    # Criando o gráfico
    indices = np.arange(len(topicos))
    largura = 0.6
    bottom = np.zeros(len(topicos))
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando as barras para cada usuário
    for uid in usuarios:
        valores = []
        for tid in topicos:
            count = sum(1 for pid in postagens 
                        if postagens[pid]['id_usuario'] == uid and 
                           postagens[pid]['id_topico'] == tid)
            valores.append(count)
        ax.bar(indices, valores, largura, label=usuarios[uid]['nome'], bottom=bottom)
        bottom += valores

    # Configurando o gráfico
    ax.set_xticks(indices)
    ax.set_xticklabels([topicos[tid]["nome"] for tid in topicos])
    ax.set_ylabel("Quantidade de Postagens")
    ax.set_title("Postagens por Tópico (Empilhado por Usuário)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()