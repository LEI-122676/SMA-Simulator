from pydoc import describe

from Item import Item


class Egg(Item):

    def __init__(self, x: int, y: int, name: str):
        super().__init__(x, y, name)
        self.is_eaten = False
        self.is_safe = False

    def describe(self):             # Estados
        status = ""

        if self.is_eaten:
            status = "Eaten"
        elif self.is_safe:
            status = "Safe"
        else:
            status = "Not eaten"

        print(f"[{self.__class__.__name__}] Name: {self.name}. Status: {status}. Location: ({self.x}, {self.y}).")

    def eat(self):
        self.is_eaten = True
        describe(self)

    def safe(self):
        self.is_safe = True
        describe(self)