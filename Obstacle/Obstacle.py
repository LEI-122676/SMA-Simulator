from abc import ABC, abstractmethod


class Obstacle(ABC):

    @abstractmethod
    def __init__(self, x: int, y: int):
        self.y = y
        self.x = x