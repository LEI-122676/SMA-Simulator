from Items.Item import Item

class Wall(Item):

    def __init__(self, id):
        super().__init__("W", id)
