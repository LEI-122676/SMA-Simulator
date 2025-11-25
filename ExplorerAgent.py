import random

from Action import Action
from Agent import Agent


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, world, learn_mode=True, steps=5000, genotype=None):
        self.id = id
        self.position = (x, y)
        self.world = world
        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]  # TODO - o genótipo sao apenas moves? ou deviam ser Actions?

        self.sensor = None
        self.observation = None

        self.behavior = set()
        self.path = []
        self.inventory = []

        self.noveltyScore = 0.0
        self.combinedFitness = 0.0
        self.step_index = 0

    def create(self, fileNameArgs):
        # TODO - something like this
        fileNameArgs = fileNameArgs.split(',')
        id = fileNameArgs[0]
        x = int(fileNameArgs[1])
        y = int(fileNameArgs[2])
        learn_mode = fileNameArgs[3].lower() == 'true'
        steps = int(fileNameArgs[4])

        return self.__init__(id, x, y, learn_mode, steps)

    def observation(self, observation):                            # Phase 5.2 TODO - isto n esta a ser usado...
        self.observation = observation

    def act(self):
        if self.step_index >= len(self.genotype):
            return None

        x, y = self.position
        mapWidth = len(self.sensor.map[0])
        mapHeight = len(self.sensor.map)

        gene = self.genotype[self.step_index]

        # TODO - aqui entra a rede neuronal? para escolher a acao a partir de 'perception'?

        return gene
        #self.behavior.add((env.agentx, env.agenty))
        #self.path.append((env.agentx, env.agenty))

    def evaluateCurrentState(self, reward):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def execute(self):
        while not self.world.solved and self.step_index < len(self.genotype):
            observation = self.sensor.get_observation(self)                          # Phase 5.1 & 5.2
            action_to_take = self.act()                                             # Phase 6

            # deliberate may return None to indicate an invalid/no-op gene that was consumed
            if action_to_take is None:
                continue

            reward = self.world.act(action_to_take, self)                           # Phase 7.1

            # consume the gene after attempting the action
            self.step_index += 1

            if reward is not None:                                                  # Phase 7.3
                self.evaluateCurrentState(reward)
                break

    def calculate_objective_fitness(self):
        """Simple objective: coverage (number of unique visited cells)."""
        return len(self.behavior)

    def mutate(self, rate: float):
        """Randomly mutate genotype: with probability rate replace a gene with a random action."""
        for i in range(len(self.genotype)):
            if random.random() < rate:
                self.genotype[i] = Action.random_action()
