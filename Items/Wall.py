from Items.Item import Item

class Wall(Item):

    def __init__(self, id, x, y):
        super().__init__("W", id, x, y)
