import random
import threading

from Item import Item
from Sensor import Sensor
from abc import ABC, abstractmethod


class Agent(threading.Thread, ABC):

    INITIAL_STEPS = 5000

    def __init__(self, id, genotype=None):
        super().__init__()
        self.id = id
        self.x = 0
        self.y = 0
        self.actions = [(0, 1),(0, -1),(-1,0),(1,0)] # N, S, W, E -> possible movements
        self.steps = self.INITIAL_STEPS # num max the steps num simulation run

        #genotype -> the sequence of actions the agent will take.
        self.genotype = genotype or [random.choice(self.actions) for _ in range(self.steps)]

        self.behavior = set() #store unique coordinates visited by the agent during a simulation, used to measure exploration
        self.path = [] #store the sequence of coordinates visited by the agent during a simulation, preserving the order

        self.noveltyScore = 0.0
        self.combinedFitness = 0.0

        self.stopEvent = threading.Event() #control flag

    def getSteps(self):
        return self.INITIAL_STEPS - self.steps

    def pickUp(self, item: Item):
        pass

    def create(self, fileNameArgs):
        pass

    def observation(self, observation):
        pass

    def act(self):
        self.steps -= 1

        currentState = self.sensor.getCurrentState(self)            # Phase 5.1
        pass

    def evaluateCurrentState(self, reward: float):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def communicate(self, message, fromAgent):
        pass

    def run(self): #Runs the agent's genotype in a fresh environment to get its behavior

        position = (0, 0) #starting position

        #reset variables
        self.behavior = set()
        self.path = []

        self.behavior.add(position)
        self.path.append(position)

        for move in self.genotype:
            if self.stopEvent.is_set():
                break

