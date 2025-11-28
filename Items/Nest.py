from Items.Item import Item


class Nest(Item):

    def __init__(self, id, x, y, capacity: int):
        super().__init__("N", id, x, y)
        self.capacity = capacity
        self.num_of_items = 0

    # Returns True when egg is put in the Nest
    def put(self, num_of_items):
        future_num_of_items = self.num_of_items + num_of_items

        if future_num_of_items < self.capacity:
            self.num_of_items = future_num_of_items
            print(f"[{self}] - Has {self.num_of_items} eggs.")
            return True
        else:
            print(f"[{self}] - Cannot put {num_of_items} eggs. Capacity is currently at {self.num_of_items}/{self.capacity}.")
            return False