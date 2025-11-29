from Agent.Chicken import Chicken
from World import World


class CoopWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.chicken_coop = None

    def initializeMap(self):
        # Posição padrão do farol no centro do mapa
        self.chicken_coop = (self.width // 2, self.height // 2)

        """
        # Colocar as galinhas -> todas lado a lado na primeira fila
        for n in range(numChickens):
            x, y = n, 0
            chicken = Chicken(n, x, y)
            self.agents.append(chicken)
            self.map[y][x] = chicken
        """

    def is_solved(self) -> bool:
        return True