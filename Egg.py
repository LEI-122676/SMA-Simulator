from Pickable import Pickable


class Egg(Pickable):

    def __init__(self, name: str, id: int, x: int, y: int):
        super().__init__(name, id, x, y)
