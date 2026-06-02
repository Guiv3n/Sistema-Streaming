from model.conteudo import Conteudo

class Serie(Conteudo):
    def __init__(self, id_conteudo: int, titulo: str, ano_lancamento: int, 
                 duracao_min: int, eh_original: bool, eh_lancamento: bool, qtd_temporadas: int):
        super().__init__(id_conteudo, titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento)
        self.qtd_temporadas = qtd_temporadas

    def exibir_detalhes(self) -> str:
        origem = "Original" if self.eh_original else "Licenciado"
        status = "Lançamento" if self.eh_lancamento else "Catálogo"
        return f"Série: {self.titulo} | {self.qtd_temporadas} Temps. | {origem} | {status}"