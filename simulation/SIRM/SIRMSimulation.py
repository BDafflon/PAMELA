import csv
import threading
import time

from agents.SIRM.standardAgent import StandardAgent
from environment.application.SIRMEnvironment.environmentSIRM import EnvironmentSIRM
from environment.application.SIRMEnvironment.standardAgentType import StandardAgentType
from environment.application.boids.environmentBoids import EnvironmentBoids
from environment.object import TargetObjet


class SIRMSimulation(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.environment = EnvironmentSIRM()
        self.path = path
        self.ready = False

    def loadDefault(self):
        self.environment.addObject(TargetObjet(0, 0))
        for i in range(0, 10):
            self.environment.addAgent(StandardAgent(1))

        for i in range(0, 2):
            self.environment.addAgent(StandardAgent(2))

        self.ready = True

    def run(self):
        if self.ready:
            self.environment.start()
        else:
            print("Erreur de simulation")
