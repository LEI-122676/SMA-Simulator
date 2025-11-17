from abc import ABC


class Item(ABC):

    def __init__(self, id, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y
        self.picked_up = False

    def pickUp(self):
        self.picked_up = True
        return f"Location: ({self.x}, {self.y})."

    def drop(self):
        self.picked_up = False
        return f"Location: ({self.x}, {self.y})."

    def __str__(self):
        return f"Item:{self.id}. Location: ({self.x}, {self.y}). Picked up: {self.picked_up}."
