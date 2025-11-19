from Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id, x, y, name):
        super().__init__("S", id, x, y)
        self.name = name
