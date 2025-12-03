from Items.Pickable import Pickable


class Egg(Pickable):

    def __init__(self, id):
        super().__init__("E", id)
