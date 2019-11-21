import pygame

from gui.gui import Gui
from simulation.simulation import Simulation


def runSimulation(path):
    s=Simulation(path)
    s.loadDefault()
    s.start()

    g = Gui(s.environment)
    g.start()


runSimulation("")
