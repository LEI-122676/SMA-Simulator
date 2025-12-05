from abc import abstractmethod

from Actions.Sensor import Sensor
from Agents.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Actions.Observation import Observation
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

    def observationFor(self, explorer: ExplorerAgent):      # Phase 5.2
        obs = Observation(explorer.id)
        sensor = explorer.sensor

        # TODO - usar Sensor?

        return explorer.observation(obs)

    """
    def crossover(self, parent1: ExplorerAgent, parent2: ExplorerAgent):
        # Performs single-point crossover on two parent genotypes.
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return ExplorerAgent(genotype=child1_geno), ExplorerAgent(genotype=child2_geno)
    """

    def act(self, action, agent: ExplorerAgent):            # Phase 7.1
        future_pos = self.is_valid_action(action, agent)
        if future_pos is None:
            return

        agent.position = future_pos
        x, y = future_pos
        obj = self.map[y][x]        

        reward = 0

        # Interaction with pickable objects
        if isinstance(obj, Pickable) and not obj.picked_up:         # Only happens on foraging world
            agent.storeItem(obj)
            reward += obj.value

        # Dropping items at nests (eggs/stones)
        elif isinstance(obj, Nest):                                 # Only happens on foraging world
            # TODO - informar outros agentes?

            totalReward = 0

            for item in agent.inventory:
                obj.put(item)
                totalReward += item.value
                agent.discardItem(item)

                self.solved = self.is_solved()              # Checks if the Eggs were all safely stored in Nests

            reward += totalReward

        # Reached the coop -> big reward                            # Only happens on chicken coop world
        elif isinstance(obj, ChickenCoop):
            reward += 100
            self.solved = self.is_solved()


        agent.evaluateCurrentState(reward)                  # Phase 7.3

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

    def add_agent(self,agent: ExplorerAgent, position):
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

    def broadcast(self, message, from_agent):
        for agent in self.agents:
            if agent != from_agent:
                agent.communicate(message)

    @abstractmethod
    def initialize_map(self):
        pass

    @abstractmethod
    def is_solved(self) -> bool:
        pass


