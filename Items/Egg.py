from Items.Pickable import Pickable


class Egg(Pickable):

    def __init__(self, id, x=0, y=0):
        # Pickable expects (name, id, x, y, value)
        super().__init__("E", id, x, y, value=100)