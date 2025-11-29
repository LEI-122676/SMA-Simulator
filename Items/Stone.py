from Items.Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id, x, y, weight: int):
        super().__init__("S", id, x, y, -2)
