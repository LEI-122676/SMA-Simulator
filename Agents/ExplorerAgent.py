from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor
from Agents.Agent import Agent
from Items.ChickenCoop import ChickenCoop
from Items.Pickable import Pickable
from Utilities import read_agent_config


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, world, learn_mode=True, steps=100, genotype=None):
        self.id = id
        self.position = (x, y)
        self.world = world

        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]

        self.sensor = None
        self.observation = None
        self.step_index = 0
        self.inventory = []

        self.coop_pos = None                    # If coop == None -> Explorer is in CoopWorld
        self.behavior = set()
        self.path = []
        
        self.combinedFitness = 0.0
        self.reward = None
        #self.noveltyScore = 0.0

    @staticmethod
    def create(file_name: str):
        """
        Create an ExplorerAgent from a configuration file.
        """
        config = read_agent_config(file_name)

        # Required fields with default fallbacks
        id = config.get("id", "0")
        x = int(config.get("x", 0)) # TODO : Confused if we get these here or in the SimulatorMotor
        y = int(config.get("y", 0)) # TODO : Confused if we get these here or in the SimulatorMotor
        learn_mode = config.get("learn_mode", "False").lower() == "true"
        steps = int(config.get("steps", 5000))

        # Optionally allow a custom genotype file
        genotype_file = config.get("genotype_file", None)
        genotype = None
        if genotype_file:
            # If file exists, read actions from it
            # For simplicity, here we just generate random actions as placeholder
            genotype = [Action.random_action() for _ in range(steps)]

        return ExplorerAgent(id, x, y, learn_mode, steps, genotype)

    def observe(self, observation: Observation): # Phase 5.2 TODO - isto n esta a ser usado...
        self.observation = observation

    def act(self) -> Action:
        if not self.learn_mode:
            return self.genotype[self.step_index]  # gene == action
        else:
            # TODO - rede neuronal! para escolher a acao a partir da 'self.observation' (i think)
            return ChickenCoop.get_action(self.coop_pos, self.position) # TODO - HARDCODED - neste momento esta a correr o que foi gerado no genotype com random actions (isto é pra mudar)


    def evaluateCurrentState(self, reward: float):
        self.reward += reward

    def install(self, sensor: Sensor):
        self.sensor = sensor
        self.coop_pos = self.sensor.get_coop_position()

    def execute(self):
        if self.step_index >= len(self.genotype):  # Agents is out of genes (actions)
            return

        # Gets observation
        observation = self.sensor.get_observation(self.id, self.position)   # Phase 5.1
        self.observe(observation)                                           # Phase 5.2

        # Decides what to do
        action_to_take = self.act()                                     # Phase 6

        # Tries to do it
        self.world.act(action_to_take, self)                            # Phase 7.1

        # Even if it fails, we count the step
        self.step_index += 1
        self.behavior.add(self.position)
        self.path.append(self.position)

    def storeItem(self, item: Pickable):
        fy, fx = item.position
        self.sensor.world.map[fy][fx] = None

        item.pickUp()
        self.inventory.append(item)

    def discardItem(self, item: Pickable):
        item.drop()
        self.inventory.append(item)


