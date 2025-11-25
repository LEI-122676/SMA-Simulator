from Agent.ExplorerAgent import ExplorerAgent


class Chicken(ExplorerAgent):

    def __init__(self, id, x, y, world):
        super().__init__(id, x ,y, world)

    def __str__(self):
        return f"C:{self.id}"