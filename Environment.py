from abc import ABC, abstractmethod

from Action import Action
from Agent import Agent
from ExplorerAgent import ExplorerAgent

class Environment(ABC):

    #@abstractmethod
    #def __init__(self, width, height):
    #    pass

    @abstractmethod
    def observationFor(self, explorer: ExplorerAgent):
        """Returns Observation"""
        pass

    @abstractmethod
    def update(self):
        """Updates the environment state"""
        pass

    @abstractmethod
    def act(self, action: Action, agent: Agent):
        pass



