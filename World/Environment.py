from abc import ABC, abstractmethod

from Actions.Action import Action
from Agent.Agent import Agent
from Agent.ExplorerAgent import ExplorerAgent
from Actions.Observation import Observation


class Environment(ABC):

    @staticmethod
    @abstractmethod
    def observationFor(self, explorer: ExplorerAgent) -> Observation:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def act(self, action: Action, agent: Agent) -> float:
        pass