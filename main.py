from gui.guiBoidsgl import GuiBoidsGL
from simulation.boids.boidsSimulation import SimulationBoids


def runSimulation(path):
    s=SimulationBoids(path)
    s.loadDefault()
    #s.start()

    g = GuiBoidsGL(s.environment)
    g.run2()


runSimulation("")
