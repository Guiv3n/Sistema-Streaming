-- Criação da tabela base de Usuários para o CRUD inicial
CREATE TABLE tb_usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    plano VARCHAR(20) NOT NULL DEFAULT 'PADRAO'
);

-- Inserindo um usuário administrador e um padrão para testes
INSERT INTO tb_usuarios (nome, email, plano) VALUES ('Admin', 'admin@stream.com', 'PREMIUM');
INSERT INTO tb_usuarios (nome, email, plano) VALUES ('Guilherme', 'gui@email.com', 'PADRAO');


CREATE TABLE tb_conteudos (
    id_conteudo SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    ano_lancamento INT NOT NULL,
    duracao_min INT NOT NULL,
    eh_original BOOLEAN NOT NULL DEFAULT FALSE,
    eh_lancamento BOOLEAN NOT NULL DEFAULT FALSE,
    tipo_conteudo VARCHAR(20) NOT NULL, -- Armazena: 'FILME', 'SERIE' ou 'ANIMACAO'
    diretor VARCHAR(100),               -- Exclusivo para Filmes
    nota_imdb NUMERIC(3,1),             -- Exclusivo para Filmes
    qtd_temporadas INT,                 -- Exclusivo para Séries
    estudio_animacao VARCHAR(100)       -- Exclusivo para Animações
);

-- Massa de dados inicial para testes no catálogo
INSERT INTO tb_conteudos (titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento, tipo_conteudo, diretor, nota_imdb) 
VALUES ('Interestelar', 2014, 169, FALSE, FALSE, 'FILME', 'Christopher Nolan', 8.7);

INSERT INTO tb_conteudos (titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento, tipo_conteudo, qtd_temporadas) 
VALUES ('Stranger Things', 2016, 50, TRUE, TRUE, 'SERIE', 4);

INSERT INTO tb_conteudos (titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento, tipo_conteudo, estudio_animacao) 
VALUES ('A Viagem de Chihiro', 2001, 125, FALSE, FALSE, 'ANIMACAO', 'Studio Ghibli');