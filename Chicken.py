from ExplorerAgent import ExplorerAgent


class Chicken(ExplorerAgent):

    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return "Chicken " + str(self.id)