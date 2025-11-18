from abc import ABC, abstractmethod

class Simulator(ABC):
    
    @abstractmethod
    def cria(self, fileNameArgs: str):
        pass

    @abstractmethod
    def listaAgentes(self):
        pass
    
    @abstractmethod
    def executa(self):
        pass