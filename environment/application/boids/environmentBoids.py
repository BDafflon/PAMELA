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


    def run(self):
        try:

            while self.running == 1:

                time.sleep(0.0002)
                self.perceptionList = {}
                self.influenceList = {}

                for agent in self.agents:
                    self.computePerception(agent)

                for agent in self.agents:
                    self.influenceList[agent.id] = None
                    self.influenceList[agent.id] = agent.update()

                self.applyInfluence()

        finally:
            print('ended')


