class Observation:

    def __init__(self, agent_id):
        self.agent_id = agent_id    # ID of the agent for whom this observation is made
        self.data = []              # Placeholder for observation data (matrix of whatever is observable from the Agent's POV)

    def addData(self, data):
        self.data.append(data)