from Sensor import Sensor


class Agent:   # Threads

    def __init__(self, id):
        self.id = id
        self.sensor = Sensor()

    def toString(self):
        return f"A{self.id}"

    def create(self, fileNameArgs):
        pass

    def observe(self, observer):
        pass

    def act(self):
        currentState = self.evaluateCurrentState(1)
        pass

    def evaluateCurrentState(self, reward):
        pass

    def install(self, sensor):
        pass

    def communicate(self, message, fromAgent):
        pass