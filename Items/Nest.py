from Items.Item import Item


class Nest(Item):

    def __init__(self, id, x, y, capacity: int):
        super().__init__("N", id, x, y)
        self.capacity = capacity
        self.num_of_items = 0

    def put(self, num_of_items):
        """ Returns True when item is put in the Nest """
        future_num_of_items = self.num_of_items + num_of_items

        if future_num_of_items < self.capacity:
            self.num_of_items = future_num_of_items
            return True

        return False