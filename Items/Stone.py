from Items.Pickable import Pickable


class Stone(Pickable):

    def __init__(self, id):
        super().__init__("S", id)
