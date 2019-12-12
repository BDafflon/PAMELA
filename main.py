from gui.guiBoidsgl import GuiBoidsGL
from gui.guiTaxisgl import GuiTaxisGL
from simulation.boids.boidsSimulation import SimulationBoids
from simulation.taxis.taxisSimulation import SimulationTaxis


def runSimulation(path):
    s = SimulationTaxis(path)

    s.loadScenario()
    s.loadTaxi()
    s.loadDestination()

    g = GuiTaxisGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return s.obsManager


o = runSimulation("./scenario/scenarioTaxiFull.csv")
o.write()
