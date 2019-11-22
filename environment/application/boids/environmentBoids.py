from environment.environment import Environment
import time



class EnvironmentBoids(Environment):
    def __init__(self):
        Environment.__init__(self)



    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                        return a
        return None

    def getFirstBoid(self):
        return self.getRandomAgent("Boid")


