import time

from Simulator.Simulator import Simulator
from World.World import World
from Utilities import read_file_parameters

class SimulatorMotor(Simulator):

    def __init__(self, time_limit=500, time_per_step=0.1):
        self.time_limit = time_limit
        self.time_per_step = time_per_step

        self.running = None
        self.world = None

        self.states = []

    def create(self, game_type, file_name_args):
        
        # TODO : NOVO FORMATO DE CONFIGURAÇÃO EM MATRIZ
        
        if game_type == "Foraging":
            try:
                config = read_file_parameters(["numEggs", "numNests", "numChickens"], file_name_args)
                numEggs = config.get("numEggs", 10)
                numNests = config.get("numNests", 2)
                numChickens = config.get("numChickens", 1)
            except Exception as e:
                print(f"Error reading configuration file: {e}")
                numEggs = 10
                numNests = 2
                numChickens = 1
        elif game_type == "Farol":
            try:
                config = read_file_parameters(["numFarols", "numChickens"], file_name_args)
                numFarols = config.get("numFarols", 3)
                numChickens = config.get("numChickens", 1)
            except Exception as e:
                print(f"Error reading configuration file: {e}")
                numFarols = 1
                numChickens = 1
        else:
            print("Unknown game type. Recognized game types are: Foraging, Farol.")

        return SimulatorMotor()

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return None

        return [a for a in self.world.chickens]

    def execute(self):
        self.running = True                                                 # Phase 1
        self.world = World()                                                # Phase 2 & 3

        while self.running:                                                 # -- loop --
            self.world.update()                                             # Phase 4

            for agent in self.world.agents:                                 # Phase 5
                agent.execute()

            self.saveState()

            # Check termination conditions
            if self.world.solved or self.time_limit == 0:                   # Phase 9
                self.running = False

            # Manage time
            self.time_limit -= self.time_per_step
            time.sleep(self.time_per_step)

        self.shutDownSimulation()                                           # Phase 10
        self.saveResults("simulation_results.txt")                          # Phase 11

    def shutDownSimulation(self):
        pass

    def saveResults(self, fileName="simulation_results.txt"):
        pass

    def saveState(self):
        # save the metrics: tempo e nr de passos, valores de novelty e fitness
        pass

if __name__ == "__main__":

    simulator = SimulatorMotor()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()