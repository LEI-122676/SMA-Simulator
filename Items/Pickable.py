from abc import abstractmethod

from Items.Item import Item


class Pickable(Item):

    def __init__(self, name, id, value=0):
        super().__init__(name, id)
        self.picked_up = None
        self.value = value

    def pickUp(self):
        self.picked_up = True
        print(f"{self} - Location: {self.position}.")

    def drop(self):
        self.picked_up = False
        print(f"{self} - Location: {self.position}.")

