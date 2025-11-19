from Item import Item


class Nest(Item):

    def __init__(self, name: str, id: int, x: int, y: int, limit: int):
        super().__init__(name, id, x, y)
        self.limit = limit
        self.eggs = 0

    # Returns True when egg is put in the Nest
    def putEgg(self, numEggs):              # TODO - synchronized
        future = self.eggs + numEggs

        if future < self.limit:
            self.eggs = future
            print(f"[{self}] - Has {self.eggs} eggs.")
            return True
        else:
            return False