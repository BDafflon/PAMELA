import threading

from agents.taxis.client import Client
from agents.taxis.taxi import Taxi
from environment.application.taxis.environmentTaxis import EnvironmentTaxis
from environment.object import Destination
from helper.observerManager import ObserverManager


class SimulationTaxis(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.environment = EnvironmentTaxis()
        self.path = path
        self.ready = False
        self.obsManager=ObserverManager("./res")

    def loadDefault(self):
        self.environment.addObject(Destination(10, 10))
        self.environment.addObject(Destination(490, 10))
        self.environment.addObject(Destination(10, 490))
        self.environment.addObject(Destination(490, 490))
        self.environment.addObject(Destination(255, 255))
        t = Taxi(self.obsManager)

        self.environment.addAgent(t)




        for i in range(1, 6):
            c= Client()
            self.environment.addAgent(c)
            self.obsManager.addObservation(c.observer)
        self.ready = True


    def run(self):
        if self.ready:
            print("START")
        else:
            print("Erreur de simulation")
