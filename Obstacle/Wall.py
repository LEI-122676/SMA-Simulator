from Obstacle import Obstacle


class Wall(Obstacle):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __str__(self):
        return "W"