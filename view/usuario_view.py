import tkinter as tk
from tkinter import ttk, messagebox
from control.usuario_controller import UsuarioController

class UsuarioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Streaming System - Gerenciamento de Usuários")
        self.root.geometry("750x500")
        
        self.controller = UsuarioController()
        
        # --- COMPONENTES DA TELA ---
        self.__criar_formulario()
        self.__criar_tabela()
        
        # Carrega os usuários existentes do banco assim que a tela abre
        self.atualizar_tabela_local()

    def __criar_formulario(self):
        frame_form = ttk.LabelFrame(self.root, text=" Cadastro de Novo Usuário / Cliente ", padding=10)
        frame_form.pack(fill="x", padx=15, pady=10)

        # Campo: Nome
        ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nome = ttk.Entry(frame_form, width=35)
        self.txt_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Campo: E-mail
        ttk.Label(frame_form, text="E-mail:").grid(row=0, column=2, sticky="w", pady=5)
        self.txt_email = ttk.Entry(frame_form, width=35)
        self.txt_email.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Campo: Plano
        ttk.Label(frame_form, text="Plano de Acesso:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_plano = ttk.Combobox(frame_form, values=["PADRAO", "PREMIUM"], state="readonly", width=15)
        self.cb_plano.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.cb_plano.set("PADRAO")

        # --- BOTÕES ---
        frame_botoes = ttk.Frame(self.root, padding=5)
        frame_botoes.pack(fill="x", padx=15)

        self.btn_salvar = ttk.Button(frame_botoes, text="Cadastrar no Banco", command=self.acao_salvar)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_excluir = ttk.Button(frame_botoes, text="Excluir Usuário Selecionado", command=self.acao_excluir)
        self.btn_excluir.pack(side="left", padx=5)

    def __criar_tabela(self):
        frame_tabela = ttk.LabelFrame(self.root, text=" Clientes Cadastrados no PostgreSQL ", padding=5)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

        colunas = ("id", "nome", "email", "plano")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Cliente")
        self.tabela.heading("email", text="E-mail de Login")
        self.tabela.heading("plano", text="Plano Ativo")

        self.tabela.column("id", width=50, anchor="center")
        self.tabela.column("nome", width=200)
        self.tabela.column("email", width=250)
        self.tabela.column("plano", width=120, anchor="center")

        self.tabela.pack(fill="both", expand=True)

    def atualizar_tabela_local(self):
        """Busca os dados atualizados na Controller e recarrega o Treeview"""
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        lista_usuarios = self.controller.listar_usuarios()
        for usr in lista_usuarios:
            self.tabela.insert("", "end", values=(
                usr.id_usuario,
                usr.nome,
                usr.email,
                usr.plano.name  # Pega o texto limpo do Enum (.name)
            ))

    def acao_salvar(self):
        nome = self.txt_nome.get()
        email = self.txt_email.get()
        plano = self.cb_plano.get()

        sucesso, mensagem = self.controller.cadastrar_usuario(nome, email, plano)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.atualizar_tabela_local()
            self.txt_nome.delete(0, tk.END)
            self.txt_email.delete(0, tk.END)
            self.cb_plano.set("PADRAO")
        else:
            messagebox.showerror("Erro de Cadastro", mensagem)

    def acao_excluir(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um usuário na tabela para remover.")
            return

        valores = self.tabela.item(selecionado[0], "values")
        id_usuario = int(valores[0])
        nome_usuario = valores[1]

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja deletar permanentemente o usuário {nome_usuario} (ID: {id_usuario})?"):
            sucesso, mensaje = self.controller.excluir_usuario(id_usuario)
            if sucesso:
                messagebox.showinfo("Sucesso", mensaje)
                self.atualizar_tabela_local()
            else:
                messagebox.showerror("Erro ao Deletar", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = UsuarioView(root)
    root.mainloop()