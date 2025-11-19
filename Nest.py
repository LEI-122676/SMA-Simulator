from Item import Item


class Nest(Item):

    def __init__(self, id, x, y, limit: int):
        super().__init__("N", id, x, y)
        self.limit = limit
        self.eggs = 0

    # Returns True when egg is put in the Nest
    def putEgg(self, numEggs):
        future = self.eggs + numEggs

        if future < self.limit:
            self.eggs = future
            print(f"[{self}] - Has {self.eggs} eggs.")
            return True
        else:
            print(f"[{self}] - Cannot put {numEggs} eggs. Limit is {self.limit}.")
            return False