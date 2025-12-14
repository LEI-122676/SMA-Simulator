from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor
from Agents.Agent import Agent
from Items.Item import Item
from Items.Pickable import Pickable
from Simulators.Utilities import read_agent_config
from Items.Nest import Nest

class ExplorerAgent(Agent):

    def __init__(self, learn_mode=True, steps=200, nn=None):
        self.position = None
        self.world = None
        self.learn_mode = learn_mode
        self.steps = steps
        self.nn = nn
        self.goal_vector = None
        self.sensor = None
        self.observation = None
        self.step_index = 0
        self.inventory: list[Pickable] = []
        self.communications = []
        self.found_nests = []
        self.behavior = set()
        self.path = []
        self.combined_fitness = 0.0
        self.reward = 0

    @classmethod
    def create(cls, file_name: str):
        config = read_agent_config(file_name)
        learn_mode = config.get("learn_mode", "False").lower() == "true"
        steps = int(config.get("steps", 5000))
        return cls(learn_mode, steps, nn=None)

    def observe(self, observation: Observation):
        self.observation = observation

    def act(self) -> Action:
        """ Delegates decision to the Neural Network if available. """
        if self.learn_mode and self.nn is not None:
            return self.nn.decide_action(self)
        return Action.random_action()

    def evaluateCurrentState(self, reward: float):
        self.reward += reward

    def install(self, sensor: Sensor, world):
        self.sensor = sensor
        self.world = world
        self.update_goal_vector()

    def update_goal_vector(self):
        if self.sensor:
            self.goal_vector = self.sensor.get_goal_vector(self.position)

    def execute(self):
        observation = self.world.observation_for(self)
        self.observe(observation)

        action_to_take = self.act()
        self.world.act(action_to_take, self)

        # Punish agent if he is stuck or oscillating based on movement history
        if len(self.path) > 0:
            if self.position == self.path[-1]:
                # Agent did not move (likely hit a wall)
                self.evaluateCurrentState(-2.0)
            elif len(self.path) > 1 and self.position == self.path[-2]:
                # Agent returned to the previous position (oscillating back and forth)
                self.evaluateCurrentState(-1.0)

        self.step_index += 1
        self.update_found_nest()
        self.behavior.add(self.position)
        self.path.append(self.position)
        self.update_goal_vector()

    def storeItem(self, item: Pickable, x, y):
        self.sensor.world_map[y][x] = None
        item.pickUp()
        self.inventory.append(item)

    def discardItem(self, item: Pickable):
        item.drop()
        if item in self.inventory:
            self.inventory.remove(item)

    def is_in_CoopWorld(self):
        return self.goal_vector is not None

    def update_found_nest(self):
        x, y = self.position
        tile = self.world.map[y][x]
        if isinstance(tile, Nest) and tile.position not in self.found_nests:
            self.found_nests.append(tile.position)

    # Legacy method stubs
    def communicate(self, item: Item, from_agent: Agent): pass
    def communicate_nest_positions(self, agents: list): return self.found_nests
    def broadcast_info(self, item: Item, agents: list): pass