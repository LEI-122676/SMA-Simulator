from Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id, x: int, y: int, name: str):
        super().__init__(id, x, y)
        self.name = name
