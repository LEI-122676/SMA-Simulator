from ExplorerAgent import ExplorerAgent


class Chicken(ExplorerAgent):

    def __init__(self, id, x, y):
        super().__init__(id, x ,y)

    def __str__(self):
        return f"C:{id}"