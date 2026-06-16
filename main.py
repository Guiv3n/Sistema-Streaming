import tkinter as tk
from tkinter import ttk
from view.usuario_view import UsuarioView
from view.catalogo_admin_view import CatalogoAdminView
from view.catalogo_cliente_view import CatalogoClienteView

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Streaming System v1.0 - Painel Integrado")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # --- ESTILIZAÇÃO COMPONENTES ---
        self.style = ttk.Style()
        self.style.configure("Menu.TButton", font=("Arial", 11, "bold"), padding=10)
        
        # --- INTERFACE ---
        self.__criar_layout()

    def __criar_layout(self):
        # Título de Boas-Vindas
        lbl_titulo = tk.Label(
            self.root, 
            text="SISTEMA DE STREAMING INTERADO\nLPOO + APS", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        lbl_titulo.pack(pady=25)
        
        # Subtítulo com os dados identificadores do projeto
        lbl_autor = tk.Label(
            self.root, 
            text="Desenvolvido por: Guilherme\nIFSul - Passo Fundo", 
            font=("Arial", 9, "italic"),
            fg="#7f8c8d"
        )
        lbl_autor.pack(pady=5)

        # Container dos Botões Centrais
        frame_botoes = ttk.Frame(self.root, padding=20)
        frame_botoes.pack(fill="both", expand=True)

        # Botão 1: Gerenciar Clientes
        btn_usuarios = ttk.Button(
            frame_botoes, 
            text="👥 GERENCIAR USUÁRIOS / PLANOS", 
            style="Menu.TButton",
            command=self.abrir_tela_usuarios
        )
        btn_usuarios.pack(fill="x", pady=8)

        # Botão 2: Painel do Admin para Mídias
        btn_catalogo_admin = ttk.Button(
            frame_botoes, 
            text="⚙️ GERENCIAR CATÁLOGO (ADMIN)", 
            style="Menu.TButton",
            command=self.abrir_tela_catalogo_admin
        )
        btn_catalogo_admin.pack(fill="x", pady=8)

        # Botão 3: Player do Cliente
        btn_catalogo_cliente = ttk.Button(
            frame_botoes, 
            text="▶️ ÁREA DO CLIENTE (SIMULAR PLAYER)", 
            style="Menu.TButton",
            command=self.abrir_tela_catalogo_cliente
        )
        btn_catalogo_cliente.pack(fill="x", pady=8)

    # --- FUNÇÕES DE NAVEGAÇÃO (Instanciam as janelas sem fechar o menu) ---
    def abrir_tela_usuarios(self):
        nova_janela = tk.Toplevel(self.root)
        UsuarioView(nova_janela)

    def abrir_tela_catalogo_admin(self):
        nova_janela = tk.Toplevel(self.root)
        CatalogoAdminView(nova_janela)

    def abrir_tela_catalogo_cliente(self):
        nova_janela = tk.Toplevel(self.root)
        CatalogoClienteView(nova_janela)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()