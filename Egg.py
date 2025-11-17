from pydoc import describe

from Item import Item


class Egg(Item):

    def __init__(self, id, x: int, y: int):
        super().__init__(id, x, y)

    def pickUp(self):
        print(f"Egg:{self.id}. ", super().pickUp())

    def drop(self):
        print(f"Egg:{self.id}. ", super().drop())
