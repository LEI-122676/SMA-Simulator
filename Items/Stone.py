from Items.Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id, x=0, y=0):
        super().__init__("S", id, x, y, value=-5)