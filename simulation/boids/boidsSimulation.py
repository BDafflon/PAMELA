import threading
from agents.boids.boids import Boid
from environment.application.boids.environmentBoids import EnvironmentBoids



class SimulationBoids(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.environment=EnvironmentBoids()
        self.path=path
        self.ready=False



    def loadDefault(self):

        for i in range(1, 10):
            self.environment.addAgent(Boid(0))
            self.environment.addAgent(Boid(1))
            self.environment.addAgent(Boid(2))
        self.ready=True

    def run(self):
        if self.ready:
            self.environment.start()
        else:
            print("Erreur de simulation")



