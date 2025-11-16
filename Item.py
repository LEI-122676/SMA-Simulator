from abc import ABC


class Item(ABC):

    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.name = name

    def pickUp(self):
        print(self.name, "was picked up!")