import tkinter as tk
from tkinter import ttk, messagebox
from control.conteudo_controller import ConteudoController
from control.usuario_controller import UsuarioController

class CatalogoClienteView:
    def __init__(self, root):
        self.root = root
        self.root.title("Streaming System - Área do Cliente")
        self.root.geometry("850x550")
        
        # Instancia ambos os controladores para amarrar as regras
        self.conteudo_ctrl = ConteudoController()
        self.usuario_ctrl = UsuarioController()
        
        # Armazena o usuário selecionado para simulação de plano
        self.usuario_atual = None
        
        # --- COMPONENTES DA INTERFACE ---
        self.__criar_seletor_usuario()
        self.__criar_barra_busca()
        self.__criar_tabela_catalogo()
        
        # Inicializa a tabela carregando o catálogo do banco
        self.atualizar_tabela_local()

    def __criar_seletor_usuario(self):
        """Painel superior para escolher com qual usuário simularemos o acesso"""
        frame_user = ttk.LabelFrame(self.root, text=" 1. Selecione o Cliente para Simular o Acesso ", padding=10)
        frame_user.pack(fill="x", padx=15, pady=5)

        ttk.Label(frame_user, text="Usuário Ativo:").grid(row=0, column=0, sticky="w")
        
        # Combobox que vai listar os usuários cadastrados no banco
        self.cb_usuarios = ttk.Combobox(frame_user, state="readonly", width=40)
        self.cb_usuarios.grid(row=0, column=1, padx=5, sticky="w")
        self.cb_usuarios.bind("<<ComboboxSelected>>", self.__acao_trocar_usuario)
        
        self.btn_atualizar_users = ttk.Button(frame_user, text="Recarregar Clientes", command=self.carregar_usuarios_no_combo)
        self.btn_atualizar_users.grid(row=0, column=2, padx=5)

        self.lbl_info_plano = ttk.Label(frame_user, text="Plano: Nenhum selecionado", font=("Arial", 10, "bold"))
        self.lbl_info_plano.grid(row=0, column=3, padx=15)
        
        # Popula o combobox com os usuários atuais do banco
        self.carregar_usuarios_no_combo()

    def __criar_barra_busca(self):
        """Barra de pesquisa por título - UC04 e RF08"""
        frame_busca = ttk.Frame(self.root, padding=5)
        frame_busca.pack(fill="x", padx=15, pady=5)

        ttk.Label(frame_busca, text="Buscar por Título:").pack(side="left", padx=5)
        
        self.txt_busca = ttk.Entry(frame_busca, width=40)
        self.txt_busca.pack(side="left", padx=5)
        
        # Evento que dispara a busca a cada tecla digitada
        self.txt_busca.bind("<KeyRelease>", self.acao_filtrar_busca)

    def __criar_tabela_catalogo(self):
        """Tabela para exibir as mídias disponíveis no PostgreSQL"""
        frame_tabela = ttk.LabelFrame(self.root, text=" 2. Catálogo Disponível (Selecione um item e clique em Assistir) ", padding=5)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

        colunas = ("id", "titulo", "tipo", "ano", "lancamento", "detalhes")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("titulo", text="Título")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("ano", text="Ano")
        self.tabela.heading("lancamento", text="Lançamento?")
        self.tabela.heading("detalhes", text="Especificações")

        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("titulo", width=200)
        self.tabela.column("tipo", width=80, anchor="center")
        self.tabela.column("ano", width=60, anchor="center")
        self.tabela.column("lancamento", width=90, anchor="center")
        self.tabela.column("detalhes", width=280)

        self.tabela.pack(fill="both", expand=True, side="left")
        
        # Barra de rolagem para a tabela
        scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        scroll.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=scroll.set)

        # Botão de Ação principal (Simular Reprodução)
        self.btn_assistir = ttk.Button(self.root, text="▶️ SIMULAR REPRODUÇÃO DE VÍDEO (UC05)", command=self.acao_assistir_video)
        self.btn_assistir.pack(pady=10)

    def carregar_usuarios_no_combo(self):
        """Busca a lista de usuários no banco e joga no Combobox"""
        self.lista_usuarios_local = self.usuario_ctrl.listar_usuarios()
        valores = [f"{u.id_usuario} - {u.nome} ({u.email})" for u in self.lista_usuarios_local]
        self.cb_usuarios["values"] = valores
        if valores:
            self.cb_usuarios.current(0)
            self.__acao_trocar_usuario()

    def __acao_trocar_usuario(self, event=None):
        """Atualiza qual usuário está ativo na simulação atual"""
        idx = self.cb_usuarios.current()
        if idx != -1:
            self.usuario_atual = self.lista_usuarios_local[idx]
            self.lbl_info_plano.config(
                text=f"Plano: {self.usuario_atual.plano.name}",
                foreground="green" if self.usuario_atual.plano.name == "PREMIUM" else "orange"
            )

    def atualizar_tabela_local(self, lista_filtrada=None):
        """Atualiza a tabela com todos os conteúdos ou com o filtro aplicado"""
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        # Se não passarmos uma lista filtrada, busca o catálogo cheio no banco
        lista = lista_filtrada if lista_filtrada is not None else self.conteudo_ctrl.listar_catalogo()
        
        for item in lista:
            self.tabela.insert("", "end", values=(
                item.id_conteudo,
                item.titulo,
                item.__class__.__name__.upper(),
                item.ano_lancamento,
                "SIM 🔥" if item.eh_lancamento else "Não",
                item.exibir_detalhes()
            ))

    def acao_filtrar_busca(self, event=None):
        """Filtra a listagem na tela conforme o texto digitado (Busca local reativa)"""
        termo = self.txt_busca.get().lower().strip()
        lista_completa = self.conteudo_ctrl.listar_catalogo()
        
        # Filtra os objetos cujo título contenha o termo digitado
        lista_filtrada = [item for item in lista_completa if termo in item.titulo.lower()]
        self.atualizar_tabela_local(lista_filtrada)

    def acao_assistir_video(self):
        """Dispara as validações do Diagrama de Sequência (RN01 e RN02)"""
        if not self.usuario_atual:
            messagebox.showwarning("Aviso", "Por favor, selecione um cliente no painel superior antes de assistir.")
            return

        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um filme, série ou animação no catálogo.")
            return

        valores = self.tabela.item(selecionado[0], "values")
        id_conteudo = int(valores[0])

        # Executa as regras de negócio RN01 e RN02 mapeadas no controlador
        permitido, mensagem = self.conteudo_ctrl.verificar_permissao_reproducao(self.usuario_atual, id_conteudo)
        
        if permitido:
            # Fluxo normal: Permissão concedida (Qualidade HD ou 4K dependendo do plano)
            messagebox.showinfo("Player de Vídeo", mensagem)
        else:
            # Fluxo de exceção: Travado pela RN01 (Usuário Padrão tentando ver Lançamento)
            messagebox.showerror("Acesso Negado (RN01)", mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoClienteView(root)
    root.mainloop()