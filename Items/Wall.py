from Items.Item import Item

class Wall(Item):

    def __init__(self, x: int, y: int):
        super().__init__("W", x, y)
