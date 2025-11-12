from Item import Item


class Stone(Item):

    def __init__(self, x: int, y: int, name: str):
        super().__init__(x, y, name)
