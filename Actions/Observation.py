class Observation:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.possible_actions = []              # ex: NORTH:2, EAST:5, SOUTH:1, WEST:0

    def total_possible_actions(self):
        count = 0

        for distance in self.possible_actions:
            count += distance

        return count