from threading import Lock


class Map:

    def __init__(self, width, height):
        self.map = [["" for _ in range(width)] for _ in range(height)]
        self.lock = Lock()
        self.solved = False

    def observationFor(self, agent):                        # Phase 5.2
        return agent.observation()

    def update(self):
        pass

    def act(self, action, agent):
        with self.lock:
            agent.num_steps += 1
