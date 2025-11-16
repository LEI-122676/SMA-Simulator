# Map.py
from Observation import Observation


class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.map = [["" for _ in range(width)] for _ in range(height)]
        self.solved = False

        # store positions of agents: {agent_id: (x,y)}
        self.positions = {}

    def observationFor(self, agent):      # Phase 5.2
        pos = self.positions[agent.id]
        return Observation(pos)

    def update(self):
        pass

    def act(self, action, agent):
        x, y = self.positions[agent.id]
        dx, dy = action

        # apply movement with boundary limits
        new_x = max(0, min(self.width - 1, x + dx))
        new_y = max(0, min(self.height - 1, y + dy))

        self.positions[agent.id] = (new_x, new_y)
