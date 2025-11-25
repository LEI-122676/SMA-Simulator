from Items.Item import Item


class ChickenCoop(Item):

    def __init__(self, id, x, y):
        super().__init__("CC", id, x, y)
