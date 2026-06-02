from conteudo import Conteudo

class Filme(Conteudo):
    def __init__(self, id_conteudo:int, titulo: str, ano_lancamento: int, duracao_min: int, eh_original: bool, eh_lancamento:bool, diretor: str, nota_imbd: float):
        super().__init__(id_conteudo, titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento)
        self.dietor = diretor
        self.nota_imdb

    def exibir_detalhes(self) ->str:
        origem = "Original" if self.eh_original else "Licenciado"
        status = "Lançamento" if self.eh_lancamento else "Catálogo"
        return f"Filme: {self.titulo} ({self.ano_lancamento}) | Diretor: {self.diretor} | {origem} | {status}"