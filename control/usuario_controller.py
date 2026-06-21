from dao.usuario_dao import UsuarioDAO
from model.usuario import Usuario
from model.plano import EnumPlano

class UsuarioController:

    def __init__(self):
        self.__dao = UsuarioDAO()

    def cadastrar_usuario(self, nome: str, email: str, plano_str: str, id_usuario: int = None) -> tuple[bool, str]:
        """Valida os dados e decide entre criar um novo cliente ou atualizar o existente"""
        if not nome.strip() or not email.strip():
            return False, "Erro: Nome e E-mail são campos obrigatórios."
        
        if "@" not in email or "." not in email:
            return False, "Erro: Digite um endereço de e-mail válido."

        try:
            plano_enum = EnumPlano[plano_str.upper()]
            
            # Instancia o objeto Usuario vinculando o ID apropriado
            novo_usuario = Usuario(id_usuario=id_usuario, nome=nome.strip(), email=email.strip(), plano=plano_enum)
            
            if id_usuario:
                return self.__dao.atualizar(novo_usuario)
            return self.__dao.salvar(novo_usuario)
            
        except KeyError:
            return False, "Erro: Plano selecionado é inválido."
        except Exception as e:
            return False, f"Erro no controlador de usuários: {e}"

    def listar_usuarios(self) -> list:
        return self.__dao.listar_todos()

    def excluir_usuario(self, id_usuario: int) -> tuple[bool, str]:
        if not id_usuario:
            return False, "Erro: Nenhum usuário selecionado."
        return self.__dao.remover(id_usuario)