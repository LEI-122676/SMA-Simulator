from Observation import Observation


class Map:

    def __init__(self, width, height):
        self.map = [["" for _ in range(width)] for _ in range(height)]
        self.solved = False

    def observationFor(self, agent):                        # Phase 5.2
        return agent.observation()

    def update(self):
        pass

    def act(self, action, agent):  # TODO - synchronized
        pass