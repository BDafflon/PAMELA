import threading

from agents.taxis.client import Client
from agents.taxis.taxi import Taxi
from environment.application.taxis.environmentTaxis import EnvironmentTaxis
from environment.object import Destination


class SimulationTaxis(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.environment=EnvironmentTaxis()
        self.path=path
        self.ready=False



    def loadDefault(self):
        self.environment.addObject(Destination(50, 50))
        self.environment.addObject(Destination(10, 10))
        self.environment.addObject(Destination(90, 10))
        self.environment.addObject(Destination(10, 90))
        self.environment.addObject(Destination(90, 90))
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



