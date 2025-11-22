from World import World
import random

from Action import Action
from ExplorerAgent import ExplorerAgent
from Egg import Egg
from Nest import Nest
from Item import Item


class ForagingWorld(World):
    """A simple foraging world: eggs are scattered on the map and nests collect eggs.

    Behavior implemented:
    - initializeMap(numEggs, numNests, ...): coloca Egg e Nest objects (sem sobreposição)
    - act(action, agent): move o agent, o agente pode recolher Eggs quando aterrar sobre eles, e deposita ovos no Ninho
    """

    def __init__(self, width=100, height=100):
        super().__init__(width, height)
        self.solved = False

    def initializeMap(self, numEggs=1, numNests=1, numChickens=1):
        self.eggs = []
        self.nests = []
        self.stones = []

        # certificar que a posição está livre
        def place_unique():
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.map[y][x] is None:
                    return x, y

        # colocar os n ovos
        for n in range(numEggs):
            x, y = place_unique()
            egg = Egg(n, x, y)
            self.eggs.append(egg)
            self.map[y][x] = egg

        # colocar os ninhos ()
        for n in range(numNests):
            x, y = place_unique()
            nest = Nest(n, x, y, capacity=1)
            self.nests.append(nest)
            self.map[y][x] = nest

        #TODO: Não utilizado ainda
        self.chickens = []

    def act(self, action, agent: ExplorerAgent):
        future_pos = self.is_valid_action(action, agent)
        if not future_pos:
            print("Invalid action attempted.")
            return
        agent.position = future_pos

        fx, fy = future_pos
        obj = self.map[fy][fx]

        # pickup egg if present and not already picked
        if isinstance(obj, Egg) and not obj.picked_up:
            agent.pickUp(obj)
            # remove from map but keep in eggs list
            self.map[fy][fx] = None

        # deposit eggs at nest
        if isinstance(obj, Nest):
            # try to deposit one egg per visit
            inventory = list(agent.inventory)
            for item in inventory:
                if isinstance(item, Egg):
                    success = obj.putEgg(1)
                    if success:
                        agent.inventory.remove(item)
                        # mark egg as delivered (optional)
                        item.position = (fx, fy)
                        item.picked_up = False

        # cada ovo tem que estar not picked_up e tem de estar num ninho da lista de ninhos para o mundo ser resolvido
        all_in_nests = all((not egg.picked_up) and any(nest.position == egg.position for nest in self.nests) for egg in self.eggs)
        
        if all_in_nests:
            self.solved = True

    # keep parent's validation logic
    def is_valid_action(self, action_to_validate: Action, explorer: ExplorerAgent):
        return super().is_valid_action(action_to_validate, explorer)
