from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.usuario import Usuario
from model.plano import EnumPlano
import psycopg2

class UsuarioDAO(GenericDAO):

    def salvar(self, usuario: Usuario) -> tuple[bool, str]:
        # =============
        # Persistência: Inserção de Usuário no Banco
        # =============
        query = "INSERT INTO tb_usuarios (nome, email, plano) VALUES (%s, %s, %s);"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (usuario.nome, usuario.email, usuario.plano.name))
            conexao.commit()
            return True, "Usuário cadastrado com sucesso!"
        except psycopg2.IntegrityError:
            return False, "Erro: Este e-mail já está cadastrado."
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro inesperado no banco: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def listar_todos(self) -> list:
        # =============
        # Persistência: Listagem Completa de Usuários
        # =============
        query = "SELECT id_usuario, nome, email, plano FROM tb_usuarios ORDER BY id_usuario;"
        conexao = None
        cursor = None
        lista_usuarios = []
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            for linha in resultados:
                # Reconstrói o objeto de domínio a partir dos dados do banco
                plano_enum = EnumPlano[linha[3]]
                usr = Usuario(id_usuario=linha[0], nome=linha[1], email=linha[2], plano=plano_enum)
                lista_usuarios.append(usr)
                
            return lista_usuarios
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def buscar_por_id(self, id_usuario: int) -> Usuario or None:
        query = "SELECT id_usuario, nome, email, plano FROM tb_usuarios WHERE id_usuario = %s;"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (id_usuario,))
            linha = cursor.fetchone()
            if linha:
                return Usuario(id_usuario=linha[0], nome=linha[1], email=linha[2], plano=EnumPlano[linha[3]])
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def atualizar(self, usuario: Usuario) -> tuple[bool, str]:
        # =============
        # Persistência: Atualização de Dados (UPDATE)
        # =============
        query = "UPDATE tb_usuarios SET nome = %s, email = %s, plano = %s WHERE id_usuario = %s;"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (usuario.nome, usuario.email, usuario.plano.name, usuario.id_usuario))
            conexao.commit()
            return True, "Usuário atualizado com sucesso!"
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def remover(self, id_usuario: int) -> tuple[bool, str]:
        # =============
        # Persistência: Remoção Física (DELETE)
        # =============
        query = "DELETE FROM tb_usuarios WHERE id_usuario = %s;"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (id_usuario,))
            conexao.commit()
            return True, "Usuário removido com sucesso!"
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro ao remover: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)