class Observation:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.possible_actions = {"North": 0, "NorthEast": 0, "East": 0, "SouthEast": 0,
                                 "South": 0, "SouthWest": 0, "West": 0, "NorthWest": 0}

    def total_possible_actions(self):
        """ Returns the total number of possible actions available (only North, East, South, West) """
        count = 0

        for direction in ["North", "East", "South", "West"]:
            if self.possible_actions[direction] > 0:
                count += 1

        return count