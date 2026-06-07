from abc import ABC, abstractmethod

class GenericDAO(ABC):
    
    @abstractmethod
    def salvar(self, objeto) -> tuple[bool, str]:
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        pass

    @abstractmethod
    def buscar_por_id(self, id_objeto: int):
        pass

    @abstractmethod
    def atualizar(self, objeto) -> tuple[bool, str]:
        pass

    @abstractmethod
    def remover(self, id_objeto: int) -> tuple[bool, str]:
        pass