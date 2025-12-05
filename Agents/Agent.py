from __future__ import annotations
from abc import ABC, abstractmethod

from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor


class Agent(ABC):

    @staticmethod
    @abstractmethod
    def create(fileNameArgs: str):
        pass

    @abstractmethod
    def observe(self, observation: Observation):
        pass

    @abstractmethod
    def act(self) -> Action:
        pass

    @abstractmethod
    def evaluateCurrentState(self, reward: float):
        pass

    @abstractmethod
    def install(self, sensor: Sensor, world):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def communicate(self, message: str, from_agent: Agent) -> str:
        pass