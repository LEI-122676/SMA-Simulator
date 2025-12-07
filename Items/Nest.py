from Items.Item import Item


class Nest(Item):

    def __init__(self, id, x=0, y=0):
        super().__init__("N", id, x, y)
        self.capacity = None
        self.num_of_items = 0

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def put(self, item):
        """ Returns True when item is put in the Nest """
        if self.capacity is None:
            raise AttributeError("Nest wasn't correctly created. capacity is None")

        if self.num_of_items + 1 <= self.capacity:
            self.num_of_items += 1
            return True
        
        if self.num_of_items == self.capacity:
            print("Nest is full!")
            print("Capacity:", self.capacity)
        
        return False