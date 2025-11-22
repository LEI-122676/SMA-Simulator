from abc import ABC, abstractmethod

from Action import Action
from Agent import Agent
from ExplorerAgent import ExplorerAgent
from Observation import Observation


class Environment(ABC):

    @staticmethod
    @abstractmethod
    def observationFor(self, explorer: ExplorerAgent) -> Observation:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def act(self, action: Action, agent: Agent):
        pass