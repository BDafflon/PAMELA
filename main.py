from gui.guiBoidsgl import GuiBoidsGL
from gui.guiTaxisgl import GuiTaxisGL
from simulation.boids.boidsSimulation import SimulationBoids
from simulation.taxis.taxisSimulation import SimulationTaxis


def runSimulation(path):
    s = SimulationTaxis(path)
    s.loadDefault()

    g = GuiTaxisGL(s.environment)
    g.run2()
    s.start()
    return s.obsManager


o = runSimulation("")
o.write()
