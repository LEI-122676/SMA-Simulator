class Observation:

    def __init__(self):
        # Dictionary storing: {Direction: (distance, ObjectType)}
        # ObjectType is the class of the object hit (e.g., Wall, Egg, None)
        self.rays = {
            "North": (0, None),
            "NorthEast": (0, None),
            "East": (0, None),
            "SouthEast": (0, None),
            "South": (0, None),
            "SouthWest": (0, None),
            "West": (0, None),
            "NorthWest": (0, None)
        }

    def add_ray(self, direction_name, distance, obj_type):
        self.rays[direction_name] = (distance, obj_type)