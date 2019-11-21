import pygame

from gui.guiTaxis import Gui
from simulation.simulation import Simulation


def runSimulation(path):
    s=Simulation(path)
    s.loadDefaultTaxis()
    s.start()

    g = Gui(s.environment)
    g.start()


runSimulation("")
