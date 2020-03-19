from gui.guiBoidsgl import GuiBoidsGL
from gui.guiSIRMgl import GuiSIRMGL
from gui.guiTaxisgl import GuiTaxisGL
from simulation.SIRM.SIRMSimulation import SIRMSimulation
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


def runSIRMSimulation(path):
    s = SIRMSimulation(path)

    s.loadDefault()

    g = GuiSIRMGL(s.environment)

    s.Gui = g
    s.start()
    g.run2()
    g.stop2()

    return []


runSIRMSimulation("")
