from gui.guiSnake import GuiSnake
from gui.guigl import GuiGL
from simulation.snake.snakeSimulation import SnakeSimulation


def runSimulation(path):
    s=SnakeSimulation(path)
    s.loadDefault()

    g = GuiSnake(s.environment)
    g.run2()


runSimulation("")
