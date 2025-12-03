from Actions.Action import Action
from Items.Item import Item


class ChickenCoop(Item):

    def __init__(self, x, y):
        super().__init__("F", 0, x, y)

    @staticmethod
    def get_action(coop_pos, explorer_position):
        """ Returns action in the direction of the coop """
        coop_x, coop_y = coop_pos
        agent_x, agent_y = explorer_position

        if coop_x < agent_x:
            return Action.MOVE_WEST         # West
        elif coop_x > agent_x:
            return Action.MOVE_EAST         # East
        elif coop_y > agent_y:
            return Action.MOVE_SOUTH        # South
        else:
            return Action.MOVE_NORTH        # North
