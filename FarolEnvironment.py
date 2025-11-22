from Environment import Environment
from Observation import Observation
from ExplorerAgent import ExplorerAgent
from Action import Action


class FarolEnvironment(Environment):
    """Simple Farol (beacon) environment.

    - grid: width x height
    - beacon: (bx, by)
    - agents move by actions (tuples or Action enum)
    """

    def __init__(self, width=20, height=20, farol_pos=None):
        self.width = width
        self.height = height
        self.solved = False

        self.map = [[None for _ in range(width)] for _ in range(height)]

        if farol_pos is None:
            bx = width - 1
            by = height - 1
            self.beacon = (bx, by)
        else:
            self.beacon = farol_pos

        self.agents = []

    def act(self, action, agent: ExplorerAgent):
        """Apply an action for an agent: support Action enum or (dx,dy) tuples.

        Update the agent position if inside bounds. If agent reaches the beacon,
        set self.solved = True.
        """
        if isinstance(action, Action):
            step = action.value
        else:
            # dando a opção de ser um tuplo (dx, dy)
            step = action

        dx, dy = step
        x, y = agent.position
        newx = x + dx
        newy = y + dy

        # não permite movimento fora dos limites
        newx = max(0, min(self.width - 1, newx))
        newy = max(0, min(self.height - 1, newy))

        agent.position = (newx, newy)

        # verifica se o agente chegou ao farol
        if agent.position == self.beacon:
            self.solved = True

    def initialize_beacon(self, beacon_pos):
        self.beacon = beacon_pos

    def isActionValid(self, future):
        x, y = future
        return 0 <= x < self.width and 0 <= y < self.height
