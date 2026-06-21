from abc import ABC, abstractmethod

class Conteudo(ABC):
    def __init__(self, id_conteudo: int, titulo: str, ano_lancamento: int, duracao_min: int, eh_original: bool, eh_lancamento: bool):
        self.id_conteudo = id_conteudo
        self.titulo = titulo
        self.ano_lancamento = ano_lancamento
        self.duracao_min = duracao_min
        self.eh_original = eh_original      # True = Original, False = Licenciado
        self.eh_lancamento = eh_lancamento  # Restrição para o plano Premium

    @abstractmethod
    def exibir_detalhes(self) -> str:
        """
        Método abstrato. Obriga as classes filhas (Filme, Serie, Animacao) 
        a implementarem suas próprias exibições de detalhes na tabela.
        """
        pass