from Sensor import Sensor


class Agent:   # Threads

    def __init__(self):
        self.actions_list = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # N, S, W, E
        self.num_steps = 0
        self.sensor = Sensor()

    def create(self, fileNameArgs):
        pass

    def observation(self, observation):
        pass

    def act(self):
        currentState = self.sensor.getCurrentState(self)            # Phase 5.1
        pass

    def evaluateCurrentState(self, reward: float):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def communicate(self, message, fromAgent):
        pass