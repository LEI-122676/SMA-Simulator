from abc import ABC


class Item(ABC):

    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.name = name

    def pickUp(self):
        print(self.name, "was picked up!")

    def __str__(self):
        return "Item: " + self.name + " at (" + str(self.x) + ", " + str(self.y) + ")"