from gui.guiBoidsgl import GuiBoidsGL
from gui.guiTaxisgl import GuiTaxisGL
from simulation.boids.boidsSimulation import SimulationBoids
from simulation.taxis.taxisSimulation import SimulationTaxis


def runSimulation(path):
    s = SimulationTaxis(path)
    s.loadDestination()
    s.loadTaxi(1)
    s.loadScenario()

    g = GuiTaxisGL(s.environment)

    s.start()
    g.run2()
    return s.obsManager


o = runSimulation("./scenario/scenario.csv")
o.write()
