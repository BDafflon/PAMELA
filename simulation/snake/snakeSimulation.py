from agents.snake.snake import Snake
from environment.environment import Environment
from environment.object import TargetObjet


class SnakeSimulation():
    def __init__(self,path):
        self.environment=Environment()
        self.path=path
        self.ready=False



    def loadDefault(self):
        self.environment.addObject(TargetObjet(0,0))
        self.environment.addAgent(Snake())
        self.ready=True
