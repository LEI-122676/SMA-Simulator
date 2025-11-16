from Map import Map


class Sensor:
    def getCurrentState(self, agent):                       # Phase 5.1
        return agent.env.observationFor(agent)
