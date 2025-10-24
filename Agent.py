class Agent:   # Threads

    def __init__(self, id):
        self.id = id

    def toString(self):
        return f"A{self.id}"

    def create(self, fileNameArgs):
        pass

    def observe(self, observer):
        pass

    def act(self):
        pass

    def evaluateCurrentState(self, reward):
        pass

    def install(self, sensor):
        pass

    def communicate(self, message, fromAgent):
        pass