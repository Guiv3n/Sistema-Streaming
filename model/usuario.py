from model.plano import EnumPlano
from model.estrategia_reproducao import EstrategiaReproducao, ReproducaoHD, Reproducao4K
from model.conteudo import Conteudo

class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str, plano: EnumPlano):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.plano = plano
        
        # Define a estratégia dinamicamente com base no plano (Mapeado no Diagrama)
        self.estrategia = None
        self.configurar_estrategia_por_plano()

    def configurar_estrategia_por_plano(self):
        """Define qual classe de reprodução este usuário usará"""
        if self.plano == EnumPlano.PREMIUM:
            self.estrategia = Reproducao4K()
        else:
            self.estrategia = ReproducaoHD()

    def assistir(self, conteudo: Conteudo) -> str:
        """Invoca o comportamento polimórfico da estratégia (Design Pattern Strategy)"""
        if self.estrategia:
            return self.estrategia.aplicar_qualidade(conteudo)
        return f"Reproduzindo '{conteudo.titulo}' em qualidade padrão..."