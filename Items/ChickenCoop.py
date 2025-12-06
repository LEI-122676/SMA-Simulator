from Actions.Action import Action
from Items.Item import Item


class ChickenCoop(Item):

    def __init__(self, x, y):
        super().__init__("F", 0)
        self.pos = (x,y)

    @staticmethod
    @staticmethod
    def get_action(target_position, explorer_position):
        coop_x, coop_y = target_position
        agent_x, agent_y = explorer_position

        # Calculate the difference vector
        dx = coop_x - agent_x
        dy = coop_y - agent_y

        if abs(dx) > abs(dy):
            return Action.MOVE_EAST if dx > 0 else Action.MOVE_WEST
        else:
            return Action.MOVE_NORTH if dy > 0 else Action.MOVE_SOUTH