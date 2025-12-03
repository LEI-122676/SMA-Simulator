from Agents.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall
from Worlds.World import World


class CoopWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.chicken_coop = None

    def initialize_map(self):
        # Posição padrão do farol no centro do mapa
        x, y = (self.width // 2, self.height // 2)
        self.chicken_coop = ChickenCoop(x, y)

        for y in range(self.height):
            for x in range(self.width):
                pass # TODO


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