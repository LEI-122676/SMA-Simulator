import random
import time

from Action import Action
from Agent import Agent


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, learn_mode=True, steps=5000, genotype=None):
        #super().__init__(id, True, steps, genotype)

        self.id = id
        self.position = (x, y)
        self.learn_mode = learn_mode
        self.steps = steps
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]

        self.sensor = None
        self.observed = set()   # store unique observations made by the agent during a simulation
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

    def observation(self, observation):
        self.observed.add(observation.getData())

    def act(self):
        """Execute a single step from the genotype. Returns the new position or None if finished."""
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

    def evaluateCurrentState(self, reward: float):
        pass

    def install(self, sensor):
        self.sensor = sensor

    def communicate(self, message, fromAgent):
        pass

    def pickUp(self, item):
        self.inventory.append(item)
        item.pickUp()
        print(f"ExplorerAgent:{self.id} picked up {item}")

    def run(self):
        # Runs the sequence of actions and requests that the Agent is responsible for

        perception = self.sensor.getCurrentState()      # Phase 5.1
        self.observation(perception)                    # Phase 5.2

        self.deliberate()                               # Phase 6

        # TODO - mudar estas cenas, decidir se corre tudo de uma vez ou todos os agentes em paralelo
        for _ in range(len(self.genotype)):
            if self.stopEvent.is_set():
                break
            self.act()
            # small sleep to avoid burning CPU in threaded runs (keeps logs readable)
            time.sleep(0)

    def deliberate(self):
        x = self.position[0]
        y = self.position[1]
        mapWidth = len(self.sensor.map[0])
        mapHeight = len(self.sensor.map)

        for action in self.genotype:
            # 1. Get new proposed position
            newx = x + action[0]
            newy = y + action[1]

            # 2. Check boundaries
            if x < 0 or x >= mapWidth or y < 0 or y >= mapHeight:
                continue

            # TODO
            # 3. Check object at new location
            #obj = env.get_object_here(newx, newy)

            # 4. Update agent/env state
            #if isinstance(obj, Ground):
                env.agentx, env.agenty = newx, newy
            #elif isinstance(obj, Key):
                env.keys.remove(obj)
                local_found_keys.append(obj)
                self.keys_found.append(obj)
                env.agentx, env.agenty = newx, newy
            #elif isinstance(obj, Treasure):
                for key in local_found_keys:
                    if key.treasure == obj.name:
                        obj.opened = True
                        env.treasures.remove(obj)
                        self.treasures_opened.append(obj)
                        env.agentx, env.agenty = newx, newy

            # 5. Record behavior
            #self.behavior.add((env.agentx, env.agenty))
            #self.path.append((env.agentx, env.agenty))

    # Convenience wrappers expected by Simulator
    def run_simulation(self):
        self.run()

    def calculate_objective_fitness(self):
        """Simple objective: coverage (number of unique visited cells)."""
        return len(self.behavior)

    def mutate(self, rate: float):
        """Randomly mutate genotype: with probability rate replace a gene with a random action."""
        for i in range(len(self.genotype)):
            if random.random() < rate:
                self.genotype[i] = Action.random_action()

    def __str__(self):
        return f"Explorer:{super().__str__()}. Inventory:{[item for item in self.inventory]}"
