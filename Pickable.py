from abc import abstractmethod

from Item import Item


class Pickable(Item):

    @abstractmethod
    def pickUp(self):
        self.picked_up = True
        print(f"{self} - Location: {self.position}.")

    @abstractmethod
    def drop(self):
        self.picked_up = False
        print(f"{self} - Location: {self.position}.")
