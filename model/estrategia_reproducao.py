from abc import ABC, abstractmethod
from model.conteudo import Conteudo

class EstrategiaReproducao(ABC):
    
    @abstractmethod
    def aplicar_qualidade(self, conteudo: Conteudo) -> str:
        pass

class ReproducaoHD(EstrategiaReproducao):
    def aplicar_qualidade(self, conteudo: Conteudo) -> str:
        return f"Reproduzindo '{conteudo.titulo}' em qualidade HD Standard (720p/1080p)..."

class Reproducao4K(EstrategiaReproducao):
    def aplicar_qualidade(self, conteudo: Conteudo) -> str:
        return f"Reproduzindo '{conteudo.titulo}' em qualidade Máxima 4K Ultra HD..."