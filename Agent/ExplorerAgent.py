import random

from Actions.Action import Action
from Agent import Agent


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, learn_mode=True, steps=5000, genotype=None):
        self.id = id
        self.position = (x, y)
        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]

        self.sensor = None
        self.observation = None
        self.step_index = 0
        self.inventory = []

        self.behavior = set()
        self.path = []
        self.reward = None
        self.noveltyScore = 0.0
        self.combinedFitness = 0.0

    def create(self, fileNameArgs):
        # TODO - read from fileNameArgs to create an ExplorerAgent
        fileNameArgs = fileNameArgs.split(',')
        id = fileNameArgs[0]
        x = int(fileNameArgs[1])
        y = int(fileNameArgs[2])
        learn_mode = fileNameArgs[3].lower() == 'true'
        steps = int(fileNameArgs[4])

        return self.__init__(id, x, y, learn_mode, steps)

    def observe(self, observation):                             # Phase 5.2 TODO - isto n esta a ser usado...
        self.observation = observation

    def act(self):
        if not self.learn_mode:
            return self.genotype[self.step_index]               # gene == action
        else:
            # TODO - rede neuronal! para escolher a acao a partir da 'self.observation' (i think)
            return self.genotype[self.step_index]  # TODO - HARDCODED - neste momento esta a correr o que foi gerado no genotype com random actions (isto é pra mudar)

    def evaluateCurrentState(self, reward):     # TODO - n sei oq isto é suposto fzr
        self.reward += reward
        pass

    def install(self, sensor):
        self.sensor = sensor

    def execute(self):
        if self.step_index >= len(self.genotype):                               # Agent is out of genes (actions)
            return

        observation = self.sensor.get_observation(self)                         # Phase 5.1
        self.observe(observation)                                               # Phase 5.2

        attempts_left = observation.total_possible_actions()

        while attempts_left > 0:                                                 # While there are still possible actions to try:
            action_to_take = self.act()                                         # Phase 6

            reward = self.sensor.world.act(action_to_take, self)                # Phase 7.1 & 7.3
            attempts_left -= 1

            if reward is not None:                                              # if reward is None -> tries to act again
                # Moved successfully
                self.evaluateCurrentState(reward)                               # Phase 7.3
                self.step_index += 1

                # Record behavior
                self.behavior.add(self.position)
                self.path.append(self.position)
                break
