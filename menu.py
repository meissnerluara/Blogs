# Importando as Bibliotecas
import os
import usuario
import topico
import postagem
import grafo_matriz_grafico

# Limpar tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Menu Principal
def menu():         
    print("BLOGS E FÓRUNS")

    print("\nMENU USUÁRIO")
    print("1. Cadastrar")
    print("2. Atualizar")
    print("3. Consultar")
    print("4. Remover")

    print("\nMENU TÓPICO")
    print("5. Criar")
    print("6. Editar")
    print("7. Visualizar")
    print("8. Excluir")

    print("\nMENU POSTAGEM")
    print("9. Criar")
    print("10. Visualizar")

    print("\nMATRIZ, GRAFO e GRÁFICO")
    print("11. Visualizar Matriz")
    print("12. Visualizar Grafo")
    print("13. Visualizar Gráfico")

    print("\nLOGOFF")
    print("14. Sair")  

# Comandos
def executar(comando):
    limpar_tela()
    print("BLOGS E FÓRUNS")
    if comando == "1":
        print("\nCadastrar Usuário\n")
        usuario.cadastar()
    elif comando == "2":
        print("\nAtualizar Usuário\n")
        usuario.atualizar()        
    elif comando == "3":
        print("\nConsultar Usuário\n")        
        usuario.consultar()      
    elif comando == "4":
        print("\nRemover Usuário\n")
        usuario.remover()

    elif comando == "5":
        print("\nCriar Tópico\n") 
        topico.criar()
    elif comando == "6":
        print("\nEditar Tópico\n")
        topico.editar()  
    elif comando == "7":
        print("\nVisualizar Tópico\n")
        topico.visualizar()  
    elif comando == "8":
        print("\nExcluir Tópico\n")
        topico.excluir()

    elif comando == "9":
        print("\nCriar Postagem\n") 
        postagem.criar() 
    elif comando == "10":
        print("\nVisualizar Postagem\n")
        postagem.visualizar()

    elif comando == "11":
        print("\nVisualizar Matriz\n")
        grafo_matriz_grafico.visualizar_matriz()
    elif comando == "12":
        print("\nVisualizar Grafo\n")
        grafo_matriz_grafico.visualizar_grafo()
    elif comando == "13":
        print("\nVisualizar Gráfico\n")
        grafo_matriz_grafico.visualizar_grafico()

    elif comando == "14":
        print("\n--- Fim do programa ---")     
    else:
        print("\nOpção inválida.")
    
    input("\nPressione qualquer tela para continuar...")

# Looping
comando = 0 
while comando != "14":
    limpar_tela()   
    menu()
    comando = input("\nEscolha uma opção: ")
    executar(comando)