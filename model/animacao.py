from model.conteudo import Conteudo

class Animacao(Conteudo):
    def __init__(self, id_conteudo: int, titulo: str, ano_lancamento: int, 
                 duracao_min: int, eh_original: bool, eh_lancamento: bool, estudio_animacao: str):
        super().__init__(id_conteudo, titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento)
        self.estudio_animacao = estudio_animacao

    def exibir_detalhes(self) -> str:
        origem = "Original" if self.eh_original else "Licenciado"
        return f"Animação: {self.titulo} | Estúdio: {self.estudio_animacao} | {origem}"