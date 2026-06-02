# Documentação de Análise e Projeto de Sistemas (APS)

## 1. Descrição e Delimitação do Escopo
O propósito deste sistema é simular o ecossistema de uma plataforma de streaming. O software resolve o problema de controle de distribuição de mídias digitais e gerenciamento de permissões de visualização baseado em assinaturas, segmentando o catálogo de forma polimórfica e aplicando travas de negócio inteligentes baseadas no perfil financeiro e técnico do cliente assinante.

## 2. Fase de Análise

### a) Requisitos Funcionais (RF)
* **RF01:** O sistema deve permitir o login diferenciado de usuários de acordo com suas credenciais (Administrador e Cliente).
* **RF02:** O sistema deve permitir ao Administrador cadastrar, listar, atualizar e remover usuários clientes.
* **RF03:** O sistema deve permitir associar cada usuário cliente a um plano específico (Padrão ou Premium).
* **RF04:** O sistema deve permitir ao Administrador gerenciar o catálogo de filmes, incluindo título, ano, duração, diretor e nota IMDB.
* **RF05:** O sistema deve permitir ao Administrador gerenciar o catálogo de séries, incluindo título, ano, duração e quantidade de temporadas.
* **RF06:** O sistema deve permitir ao Administrador gerenciar o catálogo de animações, incluindo título, ano, duração e estúdio de animação.
* **RF07:** O sistema deve permitir marcar qualquer conteúdo como "Original" ou "Licenciado".
* **RF08:** O sistema deve fornecer uma tela de listagem de conteúdos com filtros de busca por título ou tipo de mídia.
* **RF09:** O sistema deve permitir que o usuário cliente selecione e simule a reprodução de um conteúdo do catálogo compatível com as restrições do seu plano.
* **RF10:** O sistema deve permitir ao cliente adicionar conteúdos a uma lista pessoal de "Assistir Depois".

### b) Requisitos Não Funcionais (RNF)
* **RNF01:** O sistema deve utilizar o banco de dados relacional PostgreSQL para o armazenamento definitivo das entidades.
* **RNF02:** A interface com o usuário deve ser desenvolvida utilizando a biblioteca gráfica Tkinter.
* **RNF03:** O código-fonte deve ser obrigatoriamente estruturado seguindo o padrão arquitetural MVC (Model-View-Controller).
* **RNF04:** O sistema deve aplicar de forma visível os padrões de projeto Data Access Object (DAO) e Factory Method.
* **RNF05:** O sistema deve capturar exceções de persistência e exibir mensagens de alerta amigáveis (`messagebox`), evitando travamentos.

### c) Regras de Negócio (RN)
* **RN01 – Restrição de Lançamentos:** Conteúdos marcados no catálogo com a flag `eh_lancamento = True` só podem ser reproduzidos/acessados por usuários vinculados ao plano Premium.
* **RN02 – Restrição de Qualidade de Vídeo:** Clientes do plano Padrão só possuem permissão para simular a reprodução de conteúdos em qualidade convencional (SD/HD), sendo o Ultra HD (4K) de uso exclusivo do plano Premium.