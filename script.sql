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