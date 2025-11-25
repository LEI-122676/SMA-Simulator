import random
import time

from Action import Action
from Agent import Agent
from Move import Move
from Observation import Observation


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, world, learn_mode=True, steps=5000, genotype=None):
        self.id = id
        self.position = (x, y)
        self.world = world
        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = genotype or [Move.random_action() for _ in range(self.steps)]  # TODO - o genótipo sao apenas moves? ou deviam ser Actions?

        self.sensor = None
        self.observation = None
        self.behavior = set()   # store unique coordinates visited by the agent during a simulation, used to measure exploration
        self.path = []          # store the sequence of coordinates visited by the agent during a simulation, preserving the order
        self.inventory = []

        self.noveltyScore = 0.0
        self.combinedFitness = 0.0
        self.step_index = 0

    def create(self, fileNameArgs):
        """Optional factory method placeholder (not used in MVP)."""
        # TODO - something like this
        fileNameArgs = fileNameArgs.split(',')
        id = fileNameArgs[0]
        x = int(fileNameArgs[1])
        y = int(fileNameArgs[2])
        learn_mode = fileNameArgs[3].lower() == 'true'
        steps = int(fileNameArgs[4])

        return self.__init__(id, x, y, learn_mode, steps)

    def observation(self, observation):                            # Phase 5.2 TODO - isto n esta a ser usado...
        """Set the agent's observation to its current environment POV."""
        self.observation = observation
        return observation

    """    def act(self):
        # Execute a single step from the genotype. Returns the new position or None if finished.
        if self.step_index >= len(self.genotype):
            return None

        dx, dy = self.genotype[self.step_index]
        x, y = self.position
        new_pos = (x + dx, y + dy)

        self.deliberate()               # TODO - check if move is valid

        # update state
        self.position = new_pos
        self.path.append(new_pos)
        self.behavior.add(new_pos)
        self.step_index += 1
    """

    def act(self):
        pass

    def evaluateCurrentState(self, reward):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def execute(self):
        while not self.world.solved and self.step_index < len(self.genotype):
            perception = self.sensor.get_observation(self)                          # Phase 5.1 & 5.2
            action_to_take = self.deliberate(perception)                            # Phase 6

            # deliberate may return None to indicate an invalid/no-op gene that was consumed
            if action_to_take is None:
                continue

            reward = self.world.act(action_to_take, self)                           # Phase 7.1

            # consume the gene after attempting the action
            self.step_index += 1

            if reward is not None:                                                  # Phase 7.3
                self.evaluateCurrentState(reward)
                break

    def pickUp(self, item):
        self.inventory.append(item)
        item.pickUp()
        print(f"ExplorerAgent:{self.id} picked up {item}")

    def deliberate(self, perception):
        if self.step_index >= len(self.genotype) or perception is None:
            return None

        x, y = self.position
        mapWidth = len(self.sensor.map[0])
        mapHeight = len(self.sensor.map)

        gene = self.genotype[self.step_index]

        # TODO - aqui entra a rede neuronal? para escolher a acao a partir de 'perception'?

        return gene
        #self.behavior.add((env.agentx, env.agenty))
        #self.path.append((env.agentx, env.agenty))


    def calculate_objective_fitness(self):
        """Simple objective: coverage (number of unique visited cells)."""
        return len(self.behavior)

    def mutate(self, rate: float):
        """Randomly mutate genotype: with probability rate replace a gene with a random action."""
        for i in range(len(self.genotype)):
            if random.random() < rate:
                self.genotype[i] = Action.random_action()
