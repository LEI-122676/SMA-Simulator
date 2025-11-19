from abc import ABC, abstractmethod

class Simulator(ABC):
    
    @abstractmethod
    def create(self, file_name_args: str):
        """Returns Simulator"""
        pass

    @abstractmethod
    def listAgents(self):
        """Returns Agent[]"""
        pass
    
    @abstractmethod
    def execute(self):
        """Executes the simulation"""
        pass