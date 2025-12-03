from abc import ABC


class Item(ABC):

    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}{self.id}"
