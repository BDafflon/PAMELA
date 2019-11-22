from gui.guiBoids import GuiBoids
from simulation.boids.boidsSimulation import SimulationBoids


def runSimulation(path):
    s=SimulationBoids(path)
    s.loadDefault()
    s.start()

    g = GuiBoids(s.environment)
    g.start()


runSimulation("")
