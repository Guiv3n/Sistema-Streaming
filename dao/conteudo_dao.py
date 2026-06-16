from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.filme import Filme
from model.serie import Serie
from model.animacao import Animacao
from model.conteudo import Conteudo
import psycopg2

class ConteudoDAO(GenericDAO):

    def salvar(self, conteudo: Conteudo) -> tuple[bool, str]:
        # =============
        # Persistência: Inserção Polimórfica de Conteúdos
        # =============
        query = """
            INSERT INTO tb_conteudos 
            (titulo, ano_lancamento, duracao_min, eh_original, eh_lancamento, tipo_conteudo, diretor, nota_imdb, qtd_temporadas, estudio_animacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Identifica dinamicamente a classe real do objeto para extrair os atributos específicos
        tipo = conteudo.__class__.__name__.upper() # Retorna 'FILME', 'SERIE' ou 'ANIMACAO'
        
        diretor = conteudo.diretor if isinstance(conteudo, Filme) else None
        nota_imdb = conteudo.nota_imdb if isinstance(conteudo, Filme) else None
        qtd_temporadas = conteudo.qtd_temporadas if isinstance(conteudo, Serie) else None
        estudio = conteudo.estudio_animacao if isinstance(conteudo, Animacao) else None

        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (
                conteudo.titulo, conteudo.ano_lancamento, conteudo.duracao_min,
                conteudo.eh_original, conteudo.eh_lancamento, tipo,
                diretor, nota_imdb, qtd_temporadas, estudio
            ))
            conexao.commit()
            return True, f"{conteudo.__class__.__name__} cadastrado com sucesso!"
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro ao salvar conteúdo no banco: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def listar_todos(self) -> list:
        # =============
        # Persistência: Reconstrução Polimórfica vinda do PostgreSQL
        # =============
        query = "SELECT * FROM tb_conteudos ORDER BY id_conteudo;"
        conexao = None
        cursor = None
        lista_conteudos = []
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()

            for r in resultados:
                tipo = r[6] # Coluna tipo_conteudo
                
                # Instancia a classe correta baseada na string do banco
                if tipo == "FILME":
                    obj = Filme(id_conteudo=r[0], titulo=r[1], ano_lancamento=r[2], duracao_min=r[3], 
                                eh_original=r[4], eh_lancamento=r[5], diretor=r[7], nota_imdb=float(r[8]))
                elif tipo == "SERIE":
                    obj = Serie(id_conteudo=r[0], titulo=r[1], ano_lancamento=r[2], duracao_min=r[3], 
                                eh_original=r[4], eh_lancamento=r[5], qtd_temporadas=r[9])
                elif tipo == "ANIMACAO":
                    obj = Animacao(id_conteudo=r[0], titulo=r[1], ano_lancamento=r[2], duracao_min=r[3], 
                                   eh_original=r[4], eh_lancamento=r[5], estudio_animacao=r[10])
                
                lista_conteudos.append(obj)
            return lista_conteudos
        except Exception as e:
            print(f"Erro ao listar conteúdos do catálogo: {e}")
            return []
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def buscar_por_id(self, id_conteudo: int):
        query = "SELECT * FROM tb_conteudos WHERE id_conteudo = %s;"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (id_conteudo,))
            r = cursor.fetchone()
            if r:
                tipo = r[6]
                if tipo == "FILME":
                    return Filme(r[0], r[1], r[2], r[3], r[4], r[5], r[7], float(r[8]))
                elif tipo == "SERIE":
                    return Serie(r[0], r[1], r[2], r[3], r[4], r[5], r[9])
                elif tipo == "ANIMACAO":
                    return Animacao(r[0], r[1], r[2], r[3], r[4], r[5], r[10])
            return None
        except Exception as e:
            print(f"Erro ao buscar conteúdo por ID: {e}")
            return None
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def atualizar(self, conteudo: Conteudo) -> tuple[bool, str]:
        query = """
            UPDATE tb_conteudos 
            SET titulo = %s, ano_lancamento = %s, duracao_min = %s, eh_original = %s, eh_lancamento = %s,
                diretor = %s, nota_imdb = %s, qtd_temporadas = %s, estudio_animacao = %s
            WHERE id_conteudo = %s;
        """
        diretor = conteudo.diretor if isinstance(conteudo, Filme) else None
        nota_imdb = conteudo.nota_imdb if isinstance(conteudo, Filme) else None
        qtd_temporadas = conteudo.qtd_temporadas if isinstance(conteudo, Serie) else None
        estudio = conteudo.estudio_animacao if isinstance(conteudo, Animacao) else None

        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (
                conteudo.titulo, conteudo.ano_lancamento, conteudo.duracao_min,
                conteudo.eh_original, conteudo.eh_lancamento,
                diretor, nota_imdb, qtd_temporadas, estudio, conteudo.id_conteudo
            ))
            conexao.commit()
            return True, "Conteúdo do catálogo atualizado com sucesso!"
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro ao atualizar conteúdo: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)

    def remover(self, id_conteudo: int) -> tuple[bool, str]:
        query = "DELETE FROM tb_conteudos WHERE id_conteudo = %s;"
        conexao = None
        cursor = None
        try:
            conexao = DatabaseConfig.obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(query, (id_conteudo,))
            conexao.commit()
            return True, "Conteúdo removido com sucesso do catálogo!"
        except Exception as e:
            if conexao:
                conexao.rollback()
            return False, f"Erro ao remover conteúdo: {e}"
        finally:
            DatabaseConfig.fechar_recursos(conexao, cursor)