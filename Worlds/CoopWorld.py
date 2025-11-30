from Agents.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall
from Worlds.World import World


class CoopWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.chicken_coop = None

    def initializeMap(self):
        # Posição padrão do farol no centro do mapa
        x, y = (self.width // 2, self.height // 2)
        self.chicken_coop = ChickenCoop(0, x, y)

        """
        # Colocar as galinhas -> todas lado a lado na primeira fila
        for n in range(numChickens):
            x, y = n, 0
            chicken = Chicken(n, x, y)
            self.agents.append(chicken)
            self.map[y][x] = chicken
        """

    def is_solved(self) -> bool:
        for explorer in self.agents:
            if isinstance(explorer, ExplorerAgent):
                if explorer.position != self.chicken_coop_pos:
                    return False

        return True

    def showWorld(self):
        # Show the world map, agents, and the chicken coop position
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                obj = self.map[y][x]
                if any(agent.position == (x, y) for agent in self.agents):
                    row += "C "
                    continue
                elif (x, y) == self.chicken_coop_pos:
                    row += "F "
                    continue
                elif isinstance(obj, Wall):
                    row += "W "
                    continue
                else:
                    row += ". "

            print(row)
