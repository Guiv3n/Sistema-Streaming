from model.plano import EnumPlano

class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str, plano: EnumPlano = EnumPlano.PADRAO):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.plano = plano

        