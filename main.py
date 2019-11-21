import pygame

from gui.guiTaxis import GuiTaxis
from simulation.taxisSimulation import SimulationTaxis


def runSimulation(path):
    s=SimulationTaxis(path)
    s.loadDefaultTaxis()
    s.start()

    g = GuiTaxis(s.environment)
    g.start()


runSimulation("")
