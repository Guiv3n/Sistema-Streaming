from dao.usuario_dao import UsuarioDAO
from model.usuario import Usuario
from model.plano import EnumPlano

class UsuarioController:

    def __init__(self):
        self.__dao = UsuarioDAO()

    def cadastrar_usuario(self, nome: str, email: str, plano_str: str) -> tuple[bool, str]:
        """Valida os dados da tela e envia para o banco de dados"""
        # Validação de campos em branco
        if not nome.strip() or not email.strip():
            return False, "Erro: Nome e E-mail são campos obrigatórios."
        
        if "@" not in email or "." not in email:
            return False, "Erro: Digite um endereço de e-mail válido."

        try:
            # Converte a string da tela ('PADRAO' ou 'PREMIUM') para o Enum real
            plano_enum = EnumPlano[plano_str.upper()]
            
            # Instancia o modelo puro (id_usuario vai como None pois o SERIAL do Postgres resolve)
            novo_usuario = Usuario(id_usuario=None, nome=nome.strip(), email=email.strip(), plano=plano_enum)
            
            # Repassa para o DAO salvar fisicamente no PostgreSQL
            return self.__dao.salvar(novo_usuario)
            
        except KeyError:
            return False, "Erro: Plano selecionado é inválido."
        except Exception as e:
            return False, f"Erro no controlador de usuários: {e}"

    def listar_usuarios(self) -> list:
        """Retorna a lista de objetos Usuario vindos do banco"""
        return self.__dao.listar_todos()

    def excluir_usuario(self, id_usuario: int) -> tuple[bool, str]:
        if not id_usuario:
            return False, "Erro: Nenhum usuário selecionado."
        return self.__dao.remover(id_usuario)