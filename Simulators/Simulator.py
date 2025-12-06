from abc import ABC, abstractmethod

from Agents.Agent import Agent


class Simulator(ABC):

    @staticmethod
    @abstractmethod
    def create(file_name_args: str):
        pass

    @abstractmethod
    def execute(self):
        pass