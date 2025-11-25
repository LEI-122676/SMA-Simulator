from Items.Item import Item

class Farol(Item):

    def __init__(self, id, x: int, y: int, name: str, limit):
        super().__init__(id, x, y)
        self.name = name
        self.limit = limit
        self.eggs = 0