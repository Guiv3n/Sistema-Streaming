# Documentação de Análise e Projeto de Sistemas (APS)

## 1. Descrição e Delimitação do Escopo
O propósito deste sistema é simular de forma integrada o ecossistema de uma plataforma de streaming de vídeo. O software resolve o problema prático de controle de distribuição de mídias e gerenciamento de permissões de visualização baseado em perfis de assinaturas. O sistema segmenta o catálogo de mídias de forma polimórfica e aplica regras de negócio (RN) restritivas de acesso e qualidade técnica orientadas ao plano ativo do cliente simulado no momento da interação.

## 2. Fase de Análise

### a) Requisitos Funcionais (RF)
* **RF01:** O sistema deve fornecer um painel inicial integrado que possibilite o acesso chaveado às visões administrativas e de clientes.
* **RF02:** O sistema deve permitir ao Administrador manter usuários clientes (Cadastrar, Listar, Atualizar dados/planos e Remover).
* **RF03:** O sistema deve permitir associar e modificar o plano de acesso (Padrão ou Premium) de um usuário.
* **RF04:** O sistema deve permitir ao Administrador manter o catálogo de filmes, mapeando o diretor e a nota do IMDB.
* **RF05:** O sistema deve permitir ao Administrador manter o catálogo de séries, controlando a quantidade de temporadas.
* **RF06:** O sistema deve permitir ao Administrador manter o catálogo de animações, registrando o estúdio responsável.
* **RF07:** O sistema deve suportar a parametrização de flags de controle como "Conteúdo Original" e "Lançamento".
* **RF08:** O sistema deve fornecer uma tela de listagem de mídias com filtros de busca textual combinados por título e categoria (Filme, Série, Animação).
* **RF09:** O sistema deve validar dinamicamente as restrições de permissão e definir a qualidade máxima de reprodução com base no plano do usuário ativo.

### b) Requisitos Não Funcionais (RNF)
* **RNF01:** O sistema deve utilizar o banco de dados relacional PostgreSQL para o armazenamento definitivo das entidades.
* **RNF02:** A interface com o usuário deve ser desenvolvida utilizando a biblioteca gráfica nativa Tkinter.
* **RNF03:** O código-fonte deve ser estruturado seguindo o padrão arquitetural MVC (Model-View-Controller).
* **RNF04:** O sistema deve aplicar de forma explícita os padrões de projeto estruturais/comportamentais Data Access Object (DAO), Factory Method e Strategy.
* **RNF05:** O sistema deve interceptar exceções de persistência e exibindo alertas em caixas de diálogo amigáveis (`messagebox`).

### c) Regras de Negócio (RN)
* **RN01 – Restrição de Lançamentos:** Conteúdos marcados no catálogo com a flag `eh_lancamento = True` são de acesso restrito e exclusivo a usuários vinculados ao plano Premium. Tentativas de acesso por usuários do plano Padrão devem ser bloqueadas.
* **RN02 – Restrição de Qualidade de Vídeo (Strategy):** Clientes vinculados ao plano Padrão possuem a reprodução limitada à qualidade HD Standard. A liberação de streaming em qualidade Ultra HD (4K) é restrita ao plano Premium.

### d) Diagrama de Casos de Uso (Representação Textual UML)

**Atores:**
* **Administrador (Admin):** Usuário gestor que mantém os registros operacionais do catálogo e dos perfis de clientes.
* **Cliente:** Usuário que navega e simula o consumo do catálogo.

**Relações e Casos de Uso:**
* **Admin** ──> [UC01: Manter Cadastro de Clientes e Planos]
* **Admin** ──> [UC02: Manter Catálogo de Conteúdos]
* **Cliente** ──> [UC04: Buscar e Filtrar Conteúdos por Categoria]
* **Cliente** ──> [UC05: Simular Reprodução de Vídeo]

### e) Documentação de Casos de Uso (Especificação Detalhada)

#### 📑 UC02: Manter Catálogo de Conteúdos
* **Ator Principal:** Administrador
* **Pré-condições:** Nenhuma (Acesso concedido via painel de controle administrativo).
* **Fluxo Principal:**
  1. O Administrador acessa a janela de gerenciamento do catálogo.
  2. O sistema extrai e renderiza na tabela a lista de conteúdos presentes na base de dados relacional.
  3. O Administrador preenche o formulário informando a classificação da mídia (Filme, Série ou Animação), dados básicos comuns e os parâmetros específicos.
  4. O Administrador clica em "Salvar no Banco".
  5. O Controller intercepta a requisição, valida a consistência dos dados, invoca a Factory para montagem do objeto correto e solicita a persistência via DAO.
  6. O sistema exibe uma confirmação de sucesso e atualiza a tabela em tempo real.
* **Fluxos Alternativos:**
  * **Passo 3 (Alteração de Dados):** O Administrador efetua um duplo clique sobre um registro da tabela. O sistema preenche o formulário com os dados da mídia. O Admin altera os parâmetros e clica em "Atualizar no Banco". O sistema dispara um UPDATE via DAO.
  * **Passo 3 (Exclusão de Mídia):** O Administrador seleciona um conteúdo da tabela e clica em "Excluir Selecionado". O sistema solicita confirmação e executa o DELETE no banco de dados.

#### 📑 UC04: Buscar e Filtrar Conteúdos por Categoria
* **Ator Principal:** Cliente
* **Pré-condições:** Existência de mídias previamente catalogadas.
* **Fluxo Principal:**
  1. O Cliente acessa o painel de simulação da área do cliente.
  2. O sistema exibe por padrão o catálogo completo extraído do banco.
  3. O Cliente digita palavras-chave no campo de busca e/ou seleciona uma categoria específica no combo de filtros.
  4. O sistema captura os gatilhos de digitação ou seleção e atualiza dinamicamente a tabela, refinando a exibição conforme o termo de busca e tipo de mídia informados.

#### 📑 UC05: Simular Reprodução de Vídeo
* **Ator Principal:** Cliente
* **Pré-condições:** Seleção de um perfil de usuário ativo no painel de simulação e existência de mídias no catálogo.
* **Fluxo Principal:**
  1. O Cliente seleciona a mídia desejada na tabela do catálogo disponível.
  2. O Cliente clica no botão "▶️ SIMULAR REPRODUÇÃO DE VÍDEO (UC05)".
  3. A interface aciona o Controller repassando o objeto do Usuário Ativo e o ID da mídia selecionada.
  4. O Controller intercepta a chamada, requisita o modelo polimórfico ao DAO e avalia as regras de negócio restritivas.
  5. Sendo o acesso autorizado, o controlador delega a resolução técnica para a classe de modelo do Usuário, que invoca polimorficamente o padrão Strategy correspondente ao plano do assinante.
  6. O sistema exibe uma caixa de diálogo (`messagebox.showinfo`) simulando o início do streaming e informando os parâmetros de qualidade de vídeo gerados pelo Strategy.
* **Fluxo de Exceção:**
  * **Passo 4 (Violação da RN01):** Se o conteúdo for um Lançamento (`eh_lancamento = True`) e o plano do usuário selecionado for "PADRAO", o Controller interrompe o fluxo, bloqueia a execução e devolve uma mensagem descritiva. A View intercepta e renderiza um alerta de erro (`messagebox.showerror`), impedindo a simulação do player.

---

## 3. Fase de Projeto (Modelagem UML)

### a) Diagrama de Casos de Uso
*(Insira aqui a imagem do Diagrama de Casos de Uso atualizado sem o banco de dados e com as extensões do CRUD/Plano)*

### b) Diagrama de Classes
*(Insira aqui a imagem do Diagrama de Classes contendo a estrutura com a interface EstrategiaReproducao, ReproducaoHD e Reproducao4K ligadas ao Usuário)*

### c) Diagrama de Sequência
*(Insira aqui a imagem imponente do Diagrama de Sequência gerada pelo PlantUML mostrando a troca de mensagens com o bloco cinza do MVC)*