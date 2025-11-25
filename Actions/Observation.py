class Observation:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.possible_actions = []

    def addData(self, data):
        self.data.append(data)

    def getData(self):
        for d in self.data:
            yield d