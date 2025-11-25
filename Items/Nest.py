from Items.Item import Item


class Nest(Item):

    def __init__(self, id, x, y, capacity: int):
        super().__init__("N", id, x, y)
        self.capacity = capacity
        self.eggs = 0

    # Returns True when egg is put in the Nest
    def putEgg(self, numEggs):
        future = self.eggs + numEggs

        if future < self.capacity:
            self.eggs = future
            print(f"[{self}] - Has {self.eggs} eggs.")
            return True
        else:
            print(f"[{self}] - Cannot put {numEggs} eggs. Capacity is currently at {self.eggs}/{self.capacity}.")
            return False