import threading
import time
from collections import defaultdict

from Simulator import Simulator
from Terrain import Terrain


class SimulatorMotor(Simulator):

    def __init__(self, time_limit=60, time_per_step=0.5):
        self.running = None
        self.terrain = None
        self.time_limit = time_limit
        self.service_to_agents = defaultdict(set)
        self.lock = threading.Lock()
        self.time_per_step = time_per_step

    def create(self, file_name_args):
        
        #TODO : Generaliar a leitura do ficheiro de configuracao
        
        try:
            with open(file_name_args, 'r') as f: content = f.read()
            
            # Example fileNameAtgs content:
            # numEggs=15
            # numNests=3
            # numChickens=5
            
        except FileNotFoundError:
            print("file {} does not exist".format(file_name_args))
            numEggs = 10  # Default number of eggs
            numNests = 2  # Default number of nests
            numChickens = 1  # Default number of chickens
        
        content_lines = content.splitlines()
        for line in content_lines:
            key, value = line.split('=')
            key = key.strip().lower()
            value = int(value.strip())
            if key == 'numeggs':
                numEggs = value
            elif key == 'numnests':
                numNests = value
            elif key == 'numchickens':
                numChickens = value

        #self.terrain.addToMap(numEggs, numNests, numChickens)

        return Simulator

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return

        for a in self.terrain.chickens:
            yield a

    def execute(self):
        self.running = True                                                             # Phase 1
        self.terrain = Terrain()                                                        # Phase 2 & 3

        while self.running:
            self.terrain.update()                                                      # Phase 4

            # Phase 5
            for chicken in self.terrain.chickens:
                chicken.execute()

            if self.terrain.solved or self.time_limit == 0:
                self.running = False

            self.time_limit -= self.time_per_step
            time.sleep(self.time_per_step)

        self.shutDownSimulation()
        self.saveResults("simulation_results.txt")

    def shutDownSimulation(self):
        pass

    def saveResults(self, fileName="simulation_results.txt"):
        pass

if __name__ == "__main__":

    simulator = SimulatorMotor()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()