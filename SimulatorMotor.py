import concurrent.futures
import threading
import time
from collections import defaultdict

from Agent import Agent
from Map import Map
from abc import ABC, abstractmethod
from Simulator import Simulator

class SimulatorMotor(Simulator):

    def __init__(self, timeLimit=60, timePerStep=0.5):
        self.running = None
        self.map = None
        self.timeLimit = timeLimit
        self.service_to_agents = defaultdict(set)
        self.lock = threading.Lock()
        self.timePerStep = timePerStep

    def cria(self, fileNameArgs: str):
        
        #TODO : Generaliar a leitura do ficheiro de configuracao
        
        try:
            with open(fileNameArgs, 'r') as f: content = f.read()
            
            # Example fileNameAtgs content:
            # numEggs=15
            # numNests=3
            # numChickens=5
            
        except FileNotFoundError:
            print("file {} does not exist".format(fileNameArgs))
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

        self.map.addToMap(numEggs, numNests, numChickens)

        return Simulator

    def listaAgentes(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return

        for a in self.map.chickens:
            print(a)

    def executa(self):
        self.running = True                                                             # Phase 1
        self.map = Map()                                                                # Phase 2 & 3

        while self.running:
            self.map.update()                                                      # Phase 4

            # Phase 5
            for chicken in self.map.chickens:
                chicken.execute()

            if self.map.solved or self.timeLimit == 0:
                self.running = False

            self.timeLimit -= self.timePerStep
            time.sleep(self.timePerStep)

        self.shutDownSimulation()
        self.saveResults("simulation_results.txt")

    def shutDownSimulation(self):
        pass

    def saveResults(self, fileName="simulation_results.txt"):
        pass

if __name__ == "__main__":

    simulator = Simulator()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()