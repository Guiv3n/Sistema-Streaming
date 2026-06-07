import psycopg2
from psycopg2 import OperationalError

class DatabaseConfig:
    # Configuração das credenciais do banco conforme a especificação do trabalho
    __DB_NAME = "lpoo_projeto_guilherme"  # Nome padrão exigido lpoo_projeto_[nome]
    __DB_USER = "postgres"
    __DB_PASS = "postgres"
    __DB_HOST = "localhost"
    __DB_PORT = "5432"

    @classmethod
    def obter_conexao(cls):
        """Abre e retorna uma conexão ativa com o PostgreSQL"""
        try:
            conexao = psycopg2.connect(
                database=cls.__DB_NAME,
                user=cls.__DB_USER,
                password=cls.__DB_PASS,
                host=cls.__DB_HOST,
                port=cls.__DB_PORT
            )
            return conexao
        except OperationalError as e:
            print(f"[ERRO] Falha ao conectar ao banco de dados: {e}")
            raise e

    @classmethod
    def fechar_recursos(cls, conexao=None, cursor=None):
        """Fecha o cursor e a conexão de forma segura"""
        if cursor and not cursor.closed:
            cursor.close()
        if conexao and not conexao.closed:
            conexao.close()