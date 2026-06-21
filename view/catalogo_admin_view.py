import tkinter as tk
from tkinter import ttk, messagebox
from control.conteudo_controller import ConteudoController

class CatalogoAdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Streaming System - Gerenciamento do Catálogo (Admin)")
        self.root.geometry("850x600")
        
        self.controller = ConteudoController()
        self.id_em_edicao = None  # Variável de controle para o fluxo alternativo do UC02
        
        self.__criar_formulario()
        self.__criar_tabela()
        self.atualizar_tabela_local()

    def __criar_formulario(self):
        frame_form = ttk.LabelFrame(self.root, text=" Cadastro / Edição de Conteúdo ", padding=10)
        frame_form.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_form, text="Tipo:").grid(row=0, column=0, sticky="w", pady=2)
        self.cb_tipo = ttk.Combobox(frame_form, values=["FILME", "SERIE", "ANIMACAO"], state="readonly")
        self.cb_tipo.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.cb_tipo.set("FILME")
        self.cb_tipo.bind("<<ComboboxSelected>>", self.__alternar_campos_especificos)

        ttk.Label(frame_form, text="Título:").grid(row=0, column=2, sticky="w", pady=2)
        self.txt_titulo = ttk.Entry(frame_form, width=40)
        self.txt_titulo.grid(row=0, column=3, padx=5, pady=2, columnspan=3, sticky="w")

        ttk.Label(frame_form, text="Ano:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_ano = ttk.Entry(frame_form, width=10)
        self.txt_ano.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Duração (min):").grid(row=1, column=2, sticky="w", pady=2)
        self.txt_duracao = ttk.Entry(frame_form, width=10)
        self.txt_duracao.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        self.var_original = tk.BooleanVar()
        self.chk_original = ttk.Checkbutton(frame_form, text="Original", variable=self.var_original)
        self.chk_original.grid(row=1, column=4, padx=10, pady=2)

        self.var_lancamento = tk.BooleanVar()
        self.chk_lancamento = ttk.Checkbutton(frame_form, text="Lançamento", variable=self.var_lancamento)
        self.chk_lancamento.grid(row=1, column=5, padx=10, pady=2)

        self.lbl_diretor = ttk.Label(frame_form, text="Diretor:")
        self.txt_diretor = ttk.Entry(frame_form, width=20)
        self.lbl_imdb = ttk.Label(frame_form, text="Nota IMDB:")
        self.txt_imdb = ttk.Entry(frame_form, width=8)

        self.lbl_temp = ttk.Label(frame_form, text="Temporadas:")
        self.txt_temp = ttk.Entry(frame_form, width=8)

        self.lbl_estudio = ttk.Label(frame_form, text="Estúdio:")
        self.txt_estudio = ttk.Entry(frame_form, width=20)

        self.__alternar_campos_especificos()

        frame_botoes = ttk.Frame(self.root, padding=5)
        frame_botoes.pack(fill="x", padx=15)

        self.btn_salvar = ttk.Button(frame_botoes, text="Salvar no Banco", command=self.acao_salvar)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_excluir = ttk.Button(frame_botoes, text="Excluir Selecionado", command=self.acao_excluir)
        self.btn_excluir.pack(side="left", padx=5)

    def __criar_tabela(self):
        frame_tabela = ttk.LabelFrame(self.root, text=" Catálogo Cadastrado no PostgreSQL (Dê duplo clique para editar) ", padding=5)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

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
        self.tabela.bind("<Double-1>", self.acao_carregar_campos_para_edicao)

    def __alternar_campos_especificos(self, event=None):
        for widget in [self.lbl_diretor, self.txt_diretor, self.lbl_imdb, self.txt_imdb, 
                       self.lbl_temp, self.txt_temp, self.lbl_estudio, self.txt_estudio]:
            widget.grid_forget()

        tipo = self.cb_tipo.get()
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

    def acao_carregar_campos_para_edicao(self, event=None):
        """Preenche o formulário com a linha selecionada para atualização (Fluxo Alternativo UC02)"""
        selecionado = self.tabela.selection()
        if not selecionado: 
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        self.id_em_edicao = int(valores[0])
        
        lista = self.controller.listar_catalogo()
        obj = next((x for x in lista if x.id_conteudo == self.id_em_edicao), None)
        
        if obj:
            self.__limpar_campos()
            tipo_classe = obj.__class__.__name__.upper()
            self.cb_tipo.set(tipo_classe)
            self.__alternar_campos_especificos()
            
            self.txt_titulo.insert(0, obj.titulo)
            self.txt_ano.insert(0, obj.ano_lancamento)
            self.txt_duracao.insert(0, obj.duracao_min)
            self.var_original.set(obj.eh_original)
            self.var_lancamento.set(obj.eh_lancamento)
            
            if tipo_classe == "FILME":
                self.txt_diretor.insert(0, obj.diretor)
                self.txt_imdb.insert(0, obj.nota_imdb)
            elif tipo_classe == "SERIE":
                self.txt_temp.insert(0, obj.qtd_temporadas)
            elif tipo_classe == "ANIMACAO":
                self.txt_estudio.insert(0, obj.estudio_animacao)
                
            self.btn_salvar.config(text="Atualizar Dados")

    def atualizar_tabela_local(self):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        lista = self.controller.listar_catalogo()
        for item in lista:
            self.tabela.insert("", "end", values=(
                item.id_conteudo,
                item.titulo,
                item.__class__.__name__.upper(),
                item.ano_lancamento,
                f"{item.duracao_min} min",
                item.exibir_detalhes()
            ))

    def acao_salvar(self):
        dados = {
            "id_conteudo": self.id_em_edicao,  # Passa None se for novo, ou o ID ativo se for edição
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

        sucesso, mensagem = self.controller.cadastrar_conteudo(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.atualizar_tabela_local()
            self.__limpar_campos()
            self.id_em_edicao = None
            self.btn_salvar.config(text="Salvar no Banco")
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
                self.__limpar_campos()
                self.id_em_edicao = None
                self.btn_salvar.config(text="Salvar no Banco")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoAdminView(root)
    root.mainloop()