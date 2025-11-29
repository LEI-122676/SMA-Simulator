from Items.Pickable import Pickable


class Egg(Pickable):

    def __init__(self, id, x, y):
        super().__init__("E", id, x, y, 10)
