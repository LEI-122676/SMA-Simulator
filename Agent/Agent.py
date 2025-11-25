from __future__ import annotations
from abc import ABC, abstractmethod

from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor

class Agent(ABC):

    @staticmethod
    @abstractmethod
    def create(fileNameArgs: str) -> Agent:
        pass

    @abstractmethod
    def observation(self, observation: Observation):
        pass

    @abstractmethod
    def act(self) -> Action:
        pass

    @abstractmethod
    def evaluateCurrentState(self, reward: float):
        pass

    @abstractmethod
    def install(self, sensor: Sensor):
        pass

    @abstractmethod
    def execute(self):
        pass

    # "communicate" já não é preciso!