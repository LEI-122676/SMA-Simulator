from abc import ABC, abstractmethod

from Actions.Action import Action
from Agents.Agent import Agent
from Agents.ExplorerAgent import ExplorerAgent
from Actions.Observation import Observation


class Environment(ABC):

    @staticmethod
    @abstractmethod
    def observationFor(self, explorer: ExplorerAgent) -> Observation:
        pass

    @abstractmethod
    def act(self, action: Action, agent: Agent):
        pass