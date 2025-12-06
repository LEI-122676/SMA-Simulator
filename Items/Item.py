from abc import ABC


class Item(ABC):

    def __init__(self, name: str, id: int, x: int, y: int):
        self.name = name
        self.id = id
        self.position = (x,y)

    def __str__(self):
        return f"{self.name}{self.id}"
