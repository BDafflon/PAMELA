import threading

from agents.taxis.client import Client
from agents.taxis.taxi import Taxi
from environment.environment import Environment
from environment.object import Destination


class Simulation(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.environment=Environment()
        self.path=path
        self.ready=False



    def loadDefaultTaxis(self):
        self.environment.addObject(Destination(50, 50))
        self.environment.addObject(Destination(10, 10))
        self.environment.addObject(Destination(90, 10))
        self.environment.addObject(Destination(10, 90))
        t = Taxi()
        self.environment.addAgent(t)

        for i in range(1, 100):
            self.environment.addAgent(Client())
        self.ready=True

    def run(self):
        if self.ready:
            self.environment.start()
        else:
            print("Erreur de simulation")



