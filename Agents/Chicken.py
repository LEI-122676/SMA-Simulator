from Agents.ExplorerAgent import ExplorerAgent


class Chicken(ExplorerAgent):

    def __init__(self):
        super().__init__()

    def initialize_chicken_from_file(self, filename):
        super().create(self, filename)