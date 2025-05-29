CREATE DATABASE bdblog;
USE bdblog;

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