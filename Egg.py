from Pickable import Pickable


class Egg(Pickable):

    def __init__(self, id: int, x: int, y: int):
        super().__init__("E", id, x, y)