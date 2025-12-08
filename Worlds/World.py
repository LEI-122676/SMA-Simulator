import math
from abc import abstractmethod

from Actions.Sensor import Sensor
from Agents.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Items.Egg import Egg
from Items.Nest import Nest
from Items.Pickable import Pickable
from Items.Stone import Stone
from Items.Wall import Wall
from Worlds.Environment import Environment

class World(Environment):

    def __init__(self, width=30, height=30):
        self.width = width
        self.height = height
        self.solved = False
        self.map = [[None for _ in range(width)] for _ in range(height)]
        self.agents = []                                    # Phase 3

    def reset(self):
        self.solved = False
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.agents = []

    def observation_for(self, explorer: ExplorerAgent):      # Phase 5.2
        return explorer.sensor.get_observation(explorer.position)

    def act(self, action, agent: ExplorerAgent):
        # CRITICAL: Prevent NoneType unpack crash
        if agent.coop_vector is None:
            return

        future_pos = self.is_valid_action(action, agent)
        if future_pos:
            agent.position = future_pos
            agent.update_coop_vector()  # Refresh sensors immediately

            dx, dy = agent.coop_vector
            dist_now = math.sqrt(dx ** 2 + dy ** 2)

            reward = 0
            # POTENTIAL-BASED REWARD: No points for retreading tiles!
            if dist_now < agent.min_dist_reached:
                improvement = agent.min_dist_reached - dist_now
                if agent.min_dist_reached != float('inf'):
                    reward += improvement * 2.0
                agent.min_dist_reached = dist_now

            obj = self.map[agent.position[1]][agent.position[0]]
            if isinstance(obj, ChickenCoop):
                reward += 100
                self.solved = self.is_over()

            agent.evaluateCurrentState(reward)              # Phase 7.3

    def is_valid_action(self, action_to_validate, explorer):
        """ Returns None if action is invalid, or new position (x,y) if valid """

        if action_to_validate is None or explorer is None:
            return None

        dx, dy = action_to_validate.value
        px, py = explorer.position

        newx = px + dx
        newy = py + dy

        # Within bounds
        if newx < 0 or newx >= len(self.map[0]) or newy < 0 or newy >= len(self.map):
            return None
        # Check for wall at destination
        elif isinstance(self.map[newy][newx], Wall):
            return None

        return newx, newy

    def add_agent(self, agent: ExplorerAgent, position):
        agent.position = position                 # TODO - colocar o agente na posicao inicial?
        self.agents.append(agent)
        agent.install(Sensor(self.map), self)

    def show_world(self):
        # Show the world map, agents, eggs, stones, and nests
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                obj = self.map[y][x]

                if any(agent.position == (x, y) for agent in self.agents):
                    row += "C "
                elif isinstance(obj, Wall):
                    row += "W "
                elif isinstance(obj, Egg):
                    row += "E "
                elif isinstance(obj, Nest):
                    row += "N "
                elif isinstance(obj, Stone):
                    row += "S "
                elif isinstance(obj, ChickenCoop):
                    row += "F "
                else:
                    row += ". "
            print(row)
        print("\n")

    def broadcast(self, message, from_agent):
        for agent in self.agents:
            if agent != from_agent:
                agent.communicate(message)

    @abstractmethod
    def initialize_map(self, file_name):
        pass

    @abstractmethod
    def is_over(self) -> bool:
        """
        Returns True if the world is over, False otherwise
        Meaning it's over is not the same as it's solved! (all Agents could be out of steps, for example)
        """
        pass


