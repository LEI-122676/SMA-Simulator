from abc import abstractmethod

from Items.Item import Item


class Pickable(Item):

    def __init__(self, name, id, x, y, value=0):
        super().__init__(name, id, x, y)
        self.picked_up = None
        self.value = value

    @abstractmethod
    def pickUp(self):
        self.picked_up = True
        print(f"{self} - Location: {self.position}.")

    @abstractmethod
    def drop(self):
        self.picked_up = False
        print(f"{self} - Location: {self.position}.")

