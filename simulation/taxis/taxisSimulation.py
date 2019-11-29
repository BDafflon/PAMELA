import threading

from agents.taxis.client import Client
from agents.taxis.taxi import Taxi
from environment.application.taxis.environmentTaxis import EnvironmentTaxis
from environment.object import Destination


class SimulationTaxis(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.environment = EnvironmentTaxis()
        self.path = path
        self.ready = False

    def loadDefault(self):
        self.environment.addObject(Destination(10, 10))
        self.environment.addObject(Destination(490, 10))
        self.environment.addObject(Destination(10, 490))
        self.environment.addObject(Destination(490, 490))
        self.environment.addObject(Destination(255, 255))
        t = Taxi()
        self.environment.addAgent(t)

        self.environment.addAgent(Taxi())



        for i in range(1, 20):
            self.environment.addAgent(Taxi())

        for i in range(1, 200):
            self.environment.addAgent(Client())
        self.ready = True
        self.ready = True

    def run(self):
        if self.ready:
            self.environment.start()
        else:
            print("Erreur de simulation")
