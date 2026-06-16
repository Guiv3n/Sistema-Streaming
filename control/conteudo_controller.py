from dao.conteudo_dao import ConteudoDAO
from model.filme import Filme
from model.serie import Serie
from model.animacao import Animacao
from model.usuario import Usuario
from model.plano import EnumPlano

class ConteudoController:

    def __init__(self):
        self.__dao = ConteudoDAO()

    def cadastrar_conteudo(self, dados: dict) -> tuple[bool, str]:
        """
        Recebe os dados da View na forma de dicionário, valida e 
        aplica o Factory/Polimorfismo para salvar no banco.
        """
        # Validação básica de campos obrigatórios comuns
        if not dados.get("titulo") or not dados.get("ano_lancamento") or not dados.get("duracao_min"):
            return False, "Erro: Título, Ano e Duração são campos obrigatórios."

        try:
            tipo = dados.get("tipo").upper()
            
            # Padrão Factory: Instancia a classe filha correta baseada no tipo
            if tipo == "FILME":
                if not dados.get("diretor"):
                    return False, "Erro: O campo Diretor é obrigatório para Filmes."
                novo_conteudo = Filme(
                    id_conteudo=None, titulo=dados["titulo"], ano_lancamento=int(dados["ano_lancamento"]),
                    duracao_min=int(dados["duracao_min"]), eh_original=bool(dados.get("eh_original")),
                    eh_lancamento=bool(dados.get("eh_lancamento")), diretor=dados["diretor"],
                    nota_imdb=float(dados.get("nota_imdb", 0.0))
                )
                
            elif tipo == "SERIE":
                if not dados.get("qtd_temporadas"):
                    return False, "Erro: Quantidade de temporadas é obrigatória para Séries."
                novo_conteudo = Serie(
                    id_conteudo=None, titulo=dados["titulo"], ano_lancamento=int(dados["ano_lancamento"]),
                    duracao_min=int(dados["duracao_min"]), eh_original=bool(dados.get("eh_original")),
                    eh_lancamento=bool(dados.get("eh_lancamento")), qtd_temporadas=int(dados["qtd_temporadas"])
                )
                
            elif tipo == "ANIMACAO":
                if not dados.get("estudio_animacao"):
                    return False, "Erro: Estúdio de animação é obrigatório para Animações."
                novo_conteudo = Animacao(
                    id_conteudo=None, titulo=dados["titulo"], ano_lancamento=int(dados["ano_lancamento"]),
                    duracao_min=int(dados["duracao_min"]), eh_original=bool(dados.get("eh_original")),
                    eh_lancamento=bool(dados.get("eh_lancamento")), estudio_animacao=dados["estudio_animacao"]
                )
            else:
                return False, "Erro: Tipo de conteúdo inválido."

            # Chama a persistência para gravar no PostgreSQL
            return self.__dao.salvar(novo_conteudo)

        except ValueError:
            return False, "Erro: Ano, Duração, Temporadas ou Nota devem conter valores numéricos válidos."
        except Exception as e:
            return False, f"Erro no controlador: {e}"

    def listar_catalogo(self) -> list:
        """Retorna a lista completa de objetos do banco para preencher as tabelas"""
        return self.__dao.listar_todos()

    def excluir_conteudo(self, id_conteudo: int) -> tuple[bool, str]:
        if not id_conteudo:
            return False, "Erro: Nenhum conteúdo selecionado para exclusão."
        return self.__dao.remover(id_conteudo)

    def verificar_permissao_reproducao(self, usuario: Usuario, id_conteudo: int) -> tuple[bool, str]:
        """
        REGRA DE NEGÓCIO (RN01 e RN02): Valida se o plano do usuário 
        permite assistir ao conteúdo selecionado (Conforme o Diagrama de Sequência).
        """
        conteudo = self.__dao.buscar_por_id(id_conteudo)
        if not conteudo:
            return False, "Conteúdo não encontrado no catálogo."

        # RN01: Usuário do plano PADRAO não pode assistir a lançamentos
        if conteudo.eh_lancamento and usuario.plano == EnumPlano.PADRAO:
            return False, "Bloqueado: Conteúdos em lançamento são exclusivos para assinantes Premium!"

        # RN02: Define a qualidade de reprodução simulada com base no plano
        if usuario.plano == EnumPlano.PREMIUM:
            qualidade = "4K Ultra HD"
        else:
            qualidade = "HD Standard"

        return True, f"Reproduzindo '{conteudo.titulo}' em qualidade {qualidade}..."