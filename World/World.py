import random
from abc import abstractmethod

from Agent.Chicken import Chicken
from Agent.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Items.Egg import Egg
from Actions.Observation import Observation
from Items.Nest import Nest
from Items.Pickable import Pickable
from Items.Wall import Wall
from Environment import Environment


class World(Environment):

    def __init__(self, width=30, height=30):
        self.width = width
        self.height = height
        self.solved = False

        self.map = [[None for _ in range(width)] for _ in range(height)]
        self.agents = []                                    # Phase 3


    def observationFor(self, explorer: ExplorerAgent):      # Phase 5.2
        obs = Observation(explorer.id)
        sensor = explorer.sensor

        # TODO - usar Sensor?

        return explorer.observation(obs)

    def update(self):
        pass

    def act(self, action, agent: ExplorerAgent):            # Phase 7.1
        future_pos = self.is_valid_action(action, agent)
        if future_pos is None:
            return None

        agent.position = future_pos
        x, y = future_pos
        obj = self.map[y][x]                                # Object "under" the agent
        reward = 0

        # Interaction with pickable objects
        if isinstance(obj, Pickable) and not obj.picked_up:         # Only happens on foraging world
            agent.storeItem(obj)
            reward += obj.value

        # Dropping items at nests (eggs/stones)
        elif isinstance(obj, Nest):                                 # Only happens on foraging world
            totalReward = 0

            for item in agent.inventory:
                obj.put(item)
                totalReward += item.value
                agent.discardItem(item)

            reward += totalReward

        # Reached the goal -> big reward                            # Only happens on chicken coop world
        elif isinstance(obj, ChickenCoop):
            self.solved = True
            reward += 100

        return reward                                            # No reward for empty space

    def is_valid_action(self, action_to_validate, explorer):
        """ Returns None if action is invalid, or new position (x,y) if valid """

        if action_to_validate is None or explorer is None:
            return None

        dx, dy = action_to_validate
        px, py = explorer

        newx = px + dx
        newy = py + dy

        # Within bounds
        if newx < 0 or newx >= len(self.map[0]) or newy < 0 or newy >= len(self.map):
            return None
        # Check for wall at destination
        elif isinstance(self.map[newy][newx], Wall):
            return None

        return newx, newy

    @abstractmethod
    def initializeMap(self):
        pass
