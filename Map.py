class Map:

    def __init__(self, width, height):
        self.map = [["" for _ in range(width)] for _ in range(height)]
        self.solved = False

    def observerFor(self, agent):
        pass #return Observer

    def update(self):
        pass

    def act(self, action, agent):
        pass