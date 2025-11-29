from Items.Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id, x, y, weight: int):
        super().__init__("S", id, x, y, -2)
        self.weight = weight                        # The amount of space it occupies in a Nest