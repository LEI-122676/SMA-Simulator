from Observation import Observation
from Sensor import Sensor
from abc import ABC, abstractmethod


class Agent(ABC): #classe abstrata para os agentes


    #@abstractmethod
    #def __init__(self, id, learner, steps, genotype):
    #    pass

    @staticmethod
    @abstractmethod
    def create(self, fileNameArgs: str):
        """Returns Agent"""
        pass

    @abstractmethod
    def observation(self, observation: Observation):
        pass

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def evaluateCurrentState(self, reward: float):
        pass

    @abstractmethod
    def install(self, sensor: Sensor):
        pass

    # "communicate" já não é preciso!