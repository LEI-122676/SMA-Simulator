from Agents.ExplorerAgent import ExplorerAgent


class Chicken(ExplorerAgent):

    def __init__(self):
        super().__init__()

    def initialize_chicken_from_file(self, filename=None):
        if filename:
            super().create(filename)