from Sensor import Sensor


class Agent:   # Threads

    def __init__(self, id):
        self.id = id
        self.sensor = Sensor()

    def create(self, fileNameArgs):
        pass

    def observation(self, observation):
        pass

    def act(self):
        currentState = self.sensor.getCurrentState(self)
        pass

    def evaluateCurrentState(self, reward):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def communicate(self, message, fromAgent):
        pass