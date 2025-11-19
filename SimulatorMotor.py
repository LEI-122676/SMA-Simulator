import time

from Simulator import Simulator
from Terrain import Terrain


class SimulatorMotor(Simulator):


    def __init__(self, time_limit=500, time_per_step=0.1):
        self.time_limit = time_limit
        self.time_per_step = time_per_step

        self.running = None
        self.terrain = None

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


        return SimulatorMotor()

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return None

        return [a for a in self.terrain.chickens]

    def execute(self):
        self.running = True                                                 # Phase 1
        self.terrain = Terrain()                                            # Phase 2 & 3

        while self.running:                                                 # -- loop --
            self.terrain.update()                                           # Phase 4

            for chicken in self.terrain.chickens:                           # Phase 5
                chicken.execute()

            # Check termination conditions
            if self.terrain.solved or self.time_limit == 0:                 # Phase 9
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

if __name__ == "__main__":

    simulator = SimulatorMotor()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()