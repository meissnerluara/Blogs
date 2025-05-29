# Alunos Responsáveis

- Luara Godoy Meissner Pereira - 11221103634  
- Eli Makoto Higashi Matias - 11221101848

# Sobre o Projeto

Atividade 3 - M2 - Estruturas Lineares

Tema: Blogs e Fóruns

Sistema de Blog/Fórum com funcionalidades de CRUD para usuários, tópicos e postagens, integração com banco de dados MySQL, uso de IA (Cohere), e visualizações com matriz, grafo e gráfico.

# Instale as dependências:

pip install mysql-connector-python python-dotenv cohere matplotlib networkx

# Banco de Dados

Crie o banco de dados "bdblog" no MySQL Workbench com as tabelas:

CREATE TABLE usuarios (
  id_usuario INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(40) NOT NULL,
  email VARCHAR(40) UNIQUE,
  senha VARCHAR(10) NOT NULL
);

CREATE TABLE topicos (
  id_topico INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(30),
  descricao VARCHAR(100)
);

CREATE TABLE postagens (
  id_postagem INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(40),
  conteudo VARCHAR(200),
  data_publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
  id_usuario INT,
  id_topico INT,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
  FOREIGN KEY (id_topico) REFERENCES topicos(id_topico)
);

# Variáveis de Ambiente

Crie um arquivo `.env` na raiz com:

COHERE_API_KEY=sua_chave_da_cohere
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=bdblog

Como criar a Cohere API Key:

Criar conta em: https://dashboard.cohere.com/welcome/register

Depois de criar a conta e fazer login, criar API Key em: https://dashboard.cohere.com/api-keys

# IA com Cohere

No cadastro de postagens, o usuário pode optar por gerar um título automaticamente com a IA com base no conteúdo da postagem.

# Visualizações

- Interface interativa (via terminal e via Forms)
- Matriz de postagens (usuário x tópico)
- Grafo de conexões entre usuários com tópicos em comum
- Gráfico de barras de postagens por usuário
