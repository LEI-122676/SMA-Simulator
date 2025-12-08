from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor
from Agents.Agent import Agent
from Items.ChickenCoop import ChickenCoop
from Items.Item import Item
from Items.Pickable import Pickable
from Simulators.Utilities import read_agent_config
from Items.Egg import Egg
from Items.Nest import Nest


class ExplorerAgent(Agent):

    def __init__(self, learn_mode=True, steps=200, genotype=None, nn=None):
        self.position = None
        self.world = None

        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = None
        self.coop_vector = None                 # Needed for neural network

        self.sensor = None
        self.observation = None
        self.step_index = 0
        self.inventory: list[Pickable] = []
        self.communications = []                # Acho que não faz sentido para NN
        self.found_nests = []

        self.behavior = set()
        self.path = []
        self.combined_fitness = 0.0
        self.reward = 0
        self.nn = nn

    @classmethod
    def create(cls, file_name: str):
        """
        Create an ExplorerAgent from a configuration file.
        """
        config = read_agent_config(file_name)

        learn_mode = config.get("learn_mode", "False").lower() == "true"
        steps = int(config.get("steps", 5000))
        
        # Optionally allow a custom genotype file
        genotype_file = config.get("genotype_file", None)
        genotype = None
        if genotype_file:
            # TODO : genotype file logic
            # If file exists, read actions from it
            # For simplicity, here we just generate random actions as placeholder
            genotype = [Action.random_action() for _ in range(steps)]

        return cls(learn_mode, steps, genotype)

    def observe(self, observation: Observation): # Phase 5.2 TODO - isto n esta a ser usado...
        self.observation = observation

    def act(self) -> Action:
        if self.learn_mode:
            if self.nn is not None:
                return self.nn_decide_action()
            else:
                if self.coop_vector is not None:
                    return ChickenCoop.get_action(self.coop_vector, self.position)
                else:
                    return Action.random_action()
        else:
            return self.genotype[self.step_index]

    def get_nn_inputs(self):
        if self.observation is None:
            return [0.0] * 10

        inputs = []

        max_range = self.sensor.max_range
        directions = ["North", "NorthEast", "East", "SouthEast",
                      "South", "SouthWest", "West", "NorthWest"]

        for direction in directions:
            distance = self.observation.possible_actions.get(direction, 0)
            normalized_distance = distance / max_range
            inputs.append(normalized_distance)

        # se for foraging
        has_item = 1.0 if len(self.inventory) > 0 else 0.0
        inputs.append(has_item)

        # normalizacao dist to cooop
        if self.coop_vector is not None:
            coop_x, coop_y = self.coop_vector
            px, py = self.position

            dx = abs(coop_x - px)
            dy = abs(coop_y - py)
            max_dist = self.world.width + self.world.height if self.world else 60

            norm_distance = (dx + dy) / max_dist
            inputs.append(norm_distance)
        else:
            inputs.append(0.5)  # Neutral value if coop position unknown

        return inputs

    def nn_decide_action(self):
        inputs = self.get_nn_inputs()
        output = self.nn.forward(inputs)

        # Map neural network output to action
        # Output is 1 or -1 from binary step function
        if output > 0:
            # Move towards coop
            if self.coop_vector is not None:
                return ChickenCoop.get_action(self.coop_vector, self.position)
            else:
                return Action.random_action()
        else:
            # Explore randomly
            return Action.random_action()

    def evaluateCurrentState(self, reward: float):
        """ Accumulates "raw" reward during an Agent's life. """
        self.reward += reward

    def install(self, sensor: Sensor, world):
        self.sensor = sensor
        self.world = world
        self.update_coop_vector() # TODO - trocar esta funcao self.sensor.get_coop_position() & self.coop_vector tem de ser updated a cada passo (para a rede neuronal usar nos inputs)

    def update_coop_vector(self):
        self.coop_vector = self.sensor.get_coop_vector(self.position)

    def communicate(self, item: Item, from_agent: Agent):
        # Could check if it wants to accept the message or discard it according to who sent it
        message = {
            'item_name': item.name,
            'item_id': item.id,
            'item_position': item.position,
            'sender': from_agent,
        }

        self.communications.append(message)
        
    def communicate_nest_positions(self, agents: list):
        # TODO
        return self.found_nests

    def broadcast_info(self, item: Item, agents: list):
        for agent in agents:
            if agent != self:
                agent.communicate(item, self)

    def execute(self):
        if self.step_index >= len(self.genotype):  # Agents is out of genes (actions)
            return

        # Gets observation
        observation = self.world.observation_for(self)                      # Phase 5.1
        self.observe(observation)                                           # Phase 5.2

        # Decides what to do
        action_to_take = self.act()                                     # Phase 6

        # Tries to do it
        self.world.act(action_to_take, self)                            # Phase 7.1

        # Even if it fails, we count the step
        self.step_index += 1

        self.update_found_nest()
        self.behavior.add(self.position)
        self.path.append(self.position)

    def storeItem(self, item: Pickable, x, y):
        self.sensor.world_map[y][x] = None
        item.pickUp()
        self.inventory.append(item)

    def discardItem(self, item: Pickable):
        item.drop()
        if item in self.inventory:
            self.inventory.remove(item)
    
    def is_in_CoopWorld(self):
        return self.coop_vector is not None

    def update_found_nest(self):
        """
        Append new found nest positions to self.found_nests
        """
        x, y = self.position
        tile = self.world.map[y][x]
        if not isinstance(tile, Nest):
            return
        if tile.position not in self.found_nests:
            self.found_nests.append(tile.position)
            #print(f"Found nest at position: {tile.position}")