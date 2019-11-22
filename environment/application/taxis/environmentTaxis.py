from environment.environment import Environment
from agents.taxis.taxi import Taxi
import time
from agents.taxis.client import Client



class EnvironmentTaxis(Environment):
    def __init__(self):
        Environment.__init__(self)

    def getFirstTaxi(self):
        return self.getRandomAgent("Taxi")

    def run(self):
        try:

            while self.running == 1:

                time.sleep(0.0002)
                self.perceptionList = {}
                self.influenceList = {}

                for agent in self.agents:
                    self.checkStat(agent)

                for agent in self.agents:
                    self.computePerception(agent)

                for agent in self.agents:
                    self.influenceList[agent.id] = None
                    self.influenceList[agent.id] = agent.update()

                self.applyInfluence()

        finally:
            print('ended')

    def checkStat(self, a):
        if a.stat == -1:
            self.agents.remove(a)

        if isinstance(a, Client):
            if a.stat == 0:
                a.addDestination(self.getRandomObject("Destination"))

        if isinstance(a, Taxi):
            if a.stat == 0:
                d = self.getRandomAgent("Client")

                if not d == None:
                    a.addClient(d)

