from World import World

from Actions.Action import Action
from Agent.ExplorerAgent import ExplorerAgent

class FarolWorld(World):
    """A simple lighthouse world: the agent must reach the lighthouse position to solve the world.
    
    initializeMap(numEggs, numNests, ...): coloca o farol no mapa
    act(action, agent): move o agent, se o agente chegar ao farol, marca o mundo como resolvido
    """

    def initializeMap(self, numEggs, numNests, numChickens, lighthouse_pos=None):
        # utilizar iniciações de World para eggs/nests/chickens
        super().initializeMap(numEggs, numNests, numChickens)

        if lighthouse_pos is not None:
            self.lightHouse = lighthouse_pos

        lx, ly = self.lightHouse
        if 0 <= lx < self.width and 0 <= ly < self.height:
            self.map[ly][lx] = "LightHouse"


    def act(self, action, agent):
        future_pos = self.is_valid_action(action, agent)
        if not future_pos:
            return
        agent.position = future_pos

        # se o agente chegou ao farol, marcar como resolvido
        fx, fy = future_pos
        if (fx, fy) == self.lightHouse:
            self.solved = True