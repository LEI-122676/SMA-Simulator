from abc import ABC, abstractmethod
from ExplorerAgent import ExplorerAgent

class Environment(ABC):

    @abstractmethod
    def __init__(self, width, height):
        pass

    @abstractmethod
    def observationFor(self, explorer: ExplorerAgent):         # Phase 5.2
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def act(self, action, agent):
        pass



