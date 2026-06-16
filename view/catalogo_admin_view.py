import tkinter as tk
from tkinter import ttk, messagebox
from control.conteudo_controller import ConteudoController

class CatalogoAdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Streaming System - Gerenciamento do Catálogo (Admin)")
        self.root.geometry("850x600")
        
        # Instancia o controlador para fazer a ponte com o banco
        self.controller = ConteudoController()
        
        # --- COMPONENTES DA INTERFACE ---
        self.__criar_formulario()
        self.__criar_tabela()
        
        # Atualiza a tabela com os dados iniciais do banco (aquela nossa massa de testes)
        self.atualizar_tabela_local()

    def __criar_formulario(self):
        # Container principal do formulário
        frame_form = ttk.LabelFrame(self.root, text=" Cadastro / Edição de Conteúdo ", padding=10)
        frame_form.pack(fill="x", padx=15, pady=10)

        # Campo: Tipo de Conteúdo (Dita quais campos extras aparecem)
        ttk.Label(frame_form, text="Tipo:").grid(row=0, column=0, sticky="w", pady=2)
        self.cb_tipo = ttk.Combobox(frame_form, values=["FILME", "SERIE", "ANIMACAO"], state="readonly")
        self.cb_tipo.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.cb_tipo.set("FILME")
        self.cb_tipo.bind("<<ComboboxSelected>>", self.__alternar_campos_especificos)

        # Campo: Título
        ttk.Label(frame_form, text="Título:").grid(row=0, column=2, sticky="w", pady=2)
        self.txt_titulo = ttk.Entry(frame_form, width=40)
        self.txt_titulo.grid(row=0, column=3, padx=5, pady=2, columnspan=3, sticky="w")

        # Campo: Ano Lançamento
        ttk.Label(frame_form, text="Ano:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_ano = ttk.Entry(frame_form, width=10)
        self.txt_ano.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Campo: Duração (min)
        ttk.Label(frame_form, text="Duração (min):").grid(row=1, column=2, sticky="w", pady=2)
        self.txt_duracao = ttk.Entry(frame_form, width=10)
        self.txt_duracao.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # Checkboxes: Original e Lançamento
        self.var_original = tk.BooleanVar()
        self.chk_original = ttk.Checkbutton(frame_form, text="Original", variable=self.var_original)
        self.chk_original.grid(row=1, column=4, padx=10, pady=2)

        self.var_lancamento = tk.BooleanVar()
        self.chk_lancamento = ttk.Checkbutton(frame_form, text="Lançamento (Trava RN01)", variable=self.var_lancamento)
        self.chk_lancamento.grid(row=1, column=5, padx=10, pady=2)

        # --- CAMPOS ESPECÍFICOS (Vão ativar/desativar dinamicamente) ---
        # Filmes
        self.lbl_diretor = ttk.Label(frame_form, text="Diretor:")
        self.txt_diretor = ttk.Entry(frame_form, width=20)
        self.lbl_imdb = ttk.Label(frame_form, text="Nota IMDB:")
        self.txt_imdb = ttk.Entry(frame_form, width=8)

        # Séries
        self.lbl_temp = ttk.Label(frame_form, text="Temporadas:")
        self.txt_temp = ttk.Entry(frame_form, width=8)

        # Animações
        self.lbl_estudio = ttk.Label(frame_form, text="Estúdio:")
        self.txt_estudio = ttk.Entry(frame_form, width=20)

        # Inicializa exibindo os campos de Filme
        self.__alternar_campos_especificos()

        # --- PAINEL DE BOTÕES ---
        frame_botoes = ttk.Frame(self.root, padding=5)
        frame_botoes.pack(fill="x", padx=15)

        self.btn_salvar = ttk.Button(frame_botoes, text="Salvar no Banco", command=self.acao_salvar)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_excluir = ttk.Button(frame_botoes, text="Excluir Selecionado", command=self.acao_excluir)
        self.btn_excluir.pack(side="left", padx=5)

    def __criar_tabela(self):
        frame_tabela = ttk.LabelFrame(self.root, text=" Catálogo Cadastrado no PostgreSQL ", padding=5)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

        # Colunas visíveis na listagem
        colunas = ("id", "titulo", "tipo", "ano", "duracao", "detalhes")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tabela.heading("id", text="ID")
        self.tabela.heading("titulo", text="Título")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("ano", text="Ano")
        self.tabela.heading("duracao", text="Duração")
        self.tabela.heading("detalhes", text="Especificações / Detalhes")

        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("titulo", width=200)
        self.tabela.column("tipo", width=80, anchor="center")
        self.tabela.column("ano", width=60, anchor="center")
        self.tabela.column("duracao", width=80, anchor="center")
        self.tabela.column("detalhes", width=300)

        self.tabela.pack(fill="both", expand=True)

    def __alternar_campos_especificos(self, event=None):
        """Esconde os campos que não pertencem ao tipo de mídia selecionado"""
        # Esconde tudo primeiro
        for widget in [self.lbl_diretor, self.txt_diretor, self.lbl_imdb, self.txt_imdb, 
                       self.lbl_temp, self.txt_temp, self.lbl_estudio, self.txt_estudio]:
            widget.grid_forget()

        tipo = self.cb_tipo.get()
        # Posiciona na linha 2 do formulário apenas o que importa
        if tipo == "FILME":
            self.lbl_diretor.grid(row=2, column=0, sticky="w", pady=5)
            self.txt_diretor.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.lbl_imdb.grid(row=2, column=2, sticky="w", pady=5)
            self.txt_imdb.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        elif tipo == "SERIE":
            self.lbl_temp.grid(row=2, column=0, sticky="w", pady=5)
            self.txt_temp.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        elif tipo == "ANIMACAO":
            self.lbl_estudio.grid(row=2, column=0, sticky="w", pady=5)
            self.txt_estudio.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def atualizar_tabela_local(self):
        """Busca a lista atualizada na Controller e joga na tela"""
        # Limpa as linhas antigas da tabela
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        # Pede a lista atualizada para o controlador
        lista = self.controller.listar_catalogo()
        for item in lista:
            # Captura a string customizada do método exibir_detalhes() polimórfico
            detalhes = item.exibir_detalhes()
            
            self.tabela.insert("", "end", values=(
                item.id_conteudo,
                item.titulo,
                item.__class__.__name__.upper(),
                item.ano_lancamento,
                f"{item.duracao_min} min",
                detalhes
            ))

    def acao_salvar(self):
        # Monta o dicionário com os dados capturados da tela
        dados = {
            "tipo": self.cb_tipo.get(),
            "titulo": self.txt_titulo.get(),
            "ano_lancamento": self.txt_ano.get(),
            "duracao_min": self.txt_duracao.get(),
            "eh_original": self.var_original.get(),
            "eh_lancamento": self.var_lancamento.get(),
            "diretor": self.txt_diretor.get(),
            "nota_imdb": self.txt_imdb.get(),
            "qtd_temporadas": self.txt_temp.get(),
            "estudio_animacao": self.txt_estudio.get()
        }

        # Repassa para o controlador validar e salvar
        sucesso, mensagem = self.controller.cadastrar_conteudo(dados)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.atualizar_tabela_local() # Recarrega os dados na tela
            self.__limpar_campos()
        else:
            messagebox.showerror("Erro de Validação", mensagem)

    def acao_excluir(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um conteúdo na tabela para excluir.")
            return

        valores = self.tabela.item(selecionado[0], "values")
        id_remover = int(valores[0])

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o conteúdo ID {id_remover}?"):
            sucesso, mensagem = self.controller.excluir_conteudo(id_remover)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.atualizar_tabela_local()
            else:
                messagebox.showerror("Erro", mensagem)

    def __limpar_campos(self):
        self.txt_titulo.delete(0, tk.END)
        self.txt_ano.delete(0, tk.END)
        self.txt_duracao.delete(0, tk.END)
        self.txt_diretor.delete(0, tk.END)
        self.txt_imdb.delete(0, tk.END)
        self.txt_temp.delete(0, tk.END)
        self.txt_estudio.delete(0, tk.END)
        self.var_original.set(False)
        self.var_lancamento.set(False)

# Bloco de execução isolado para testar a janela abrindo sozinha
if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoAdminView(root)
    root.mainloop()