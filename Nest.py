from Item import Item


class Nest(Item):

    def __init__(self, id, x: int, y: int, name: str, limit):
        super().__init__(id, x, y)
        self.name = name
        self.limit = limit
        self.eggs = 0

    # Returns True when egg is put in the Nest
    def putEgg(self, numEggs):              # TODO - synchronized
        if self.eggs < self.limit:
            self.eggs += numEggs

            print(f"[{self.__class__.__name__}] Name: {self.name}. Status: {self.eggs}. Location: ({self.x}, {self.y}).")
            return True
        else:
            return False