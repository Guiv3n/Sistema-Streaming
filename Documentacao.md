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

* ### d) Diagrama de Casos de Uso (Representação Textual UML)

**Atores:**
* **Administrador (Admin):** Usuário interno responsável pela gestão e manutenção do catálogo e clientes.
* **Cliente:** Usuário final que consome as mídias da plataforma de streaming (segmentado em Padrão e Premium).

**Relações e Casos de Uso:**
* **Admin** ──> [UC01: Manter Clientes]
* **Admin** ──> [UC02: Manter Catálogo de Conteúdos]
* **Cliente** ──> [UC03: Autenticar no Sistema]
* **Cliente** ──> [UC04: Buscar e Filtrar Conteúdos]
* **Cliente** ──> [UC05: Simular Reprodução de Vídeo]
* [UC05: Simular Reprodução de Vídeo] ──> <<include>> ──> [UC03: Autenticar no Sistema]

### e) Documentação de Casos de Uso (Especificação Detalhada)

Aqui estão especificados os casos de uso principais para o entendimento e rastreabilidade da arquitetura do sistema:

#### 📑 UC02: Manter Catálogo de Conteúdos
* **Ator Principal:** Administrador
* **Pré-condições:** O Administrador deve estar autenticado no sistema.
* **Fluxo Principal:**
  1. O Administrador acessa a tela de gerenciamento do catálogo.
  2. O sistema exibe a lista de conteúdos cadastrados (Filmes, Séries e Animações).
  3. O Administrador seleciona a opção "Inserir Novo Conteúdo".
  4. O Administrador define o tipo (Filme, Série ou Animação) e preenche os campos obrigatórios (Título, Ano, Duração, flags Original/Licenciado e Lançamento), além dos atributos específicos do tipo.
  5. O Administrador clica em "Salvar".
  6. O sistema valida os dados através do Controller, invoca o Factory Method para instanciar o objeto correto e solicita ao DAO a persistência no PostgreSQL.
  7. O sistema exibe uma mensagem de sucesso e atualiza a listagem em tela.
* **Fluxos Alternativos:**
  * **Passo 3 (Alteração):** O Admin seleciona um conteúdo existente, altera os dados e clica em "Atualizar". O sistema valida e salva as alterações via UPDATE no banco de dados.
  * **Passo 3 (Exclusão):** O Admin seleciona um conteúdo existente e clica em "Remover". O sistema solicita confirmação e executa o DELETE via DAO.
* **Fluxo de Exceção:**
  * **Passo 6 (Dados Inválidos):** Se algum campo obrigatório estiver vazio ou com formato incorreto (ex: taxa numérica ou ano inválido), o Controller captura a exceção e exibe uma `messagebox` com o erro, retornando ao passo 4 sem fechar a janela.

#### 📑 UC04: Buscar e Filtrar Conteúdos
* **Ator Principal:** Cliente
* **Pré-condições:** Nenhuma (Acesso ao catálogo de exibição).
* **Fluxo Principal:**
  1. O Cliente abre a interface de catálogo da aplicação.
  2. O sistema carrega e exibe todos os títulos disponíveis vindos da tabela do banco de dados.
  3. O Cliente digita um termo no campo de busca por título ou seleciona um filtro específico (ex: Apenas Filmes, Séries ou Animações).
  4. O Cliente clica no botão "Buscar".
  5. O Controller intercepta a requisição, formata a string de busca de forma defensiva e aciona o método de busca por filtros do DAO.
  6. O sistema atualiza o componente visual (`Treeview`) mostrando apenas os resultados correspondentes.
* **Pós-condições:** O catálogo é filtrado dinamicamente na tela do usuário.

#### 📑 UC05: Simular Reprodução de Vídeo
* **Ator Principal:** Cliente
* **Pré-condições:** O Cliente deve estar autenticado no sistema e com um plano (Padrão ou Premium) ativo.
* **Fluxo Principal:**
  1. O Cliente seleciona um conteúdo desejado na listagem do catálogo.
  2. O Cliente clica no botão "Assistir / Reproduzir".
  3. O sistema verifica as Regras de Negócio (RN01 e RN02) comparando as propriedades do conteúdo com o plano do usuário.
  4. Sendo o conteúdo permitido para o plano do usuário, o sistema abre uma janela de simulação exibindo o player com a qualidade máxima correspondente (HD para Padrão, 4K para Premium).
* **Fluxo de Exceção (Bloqueio por Regra de Negócio):**
  * **Passo 3 (Violação da RN01):** Se o conteúdo for um Lançamento (`eh_lancamento = True`) e o plano do usuário for "Padrão", o sistema bloqueia a reprodução e exibe a mensagem: *"Conteúdo exclusivo para assinantes do Plano Premium. Faça o upgrade para assistir."*