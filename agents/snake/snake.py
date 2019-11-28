import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.boids.boidsBody import BoidsBody
from environment.application.snake.snakeBody import SnakeBody
from helper import util
from helper.vector2D import Vector2D


class Snake(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.body = SnakeBody()
        self.type = "Snake"
        self.body.fustrum.radius = 100

    def moveRandom(self):
        x = int(random.uniform(-200, 200))
        y = int(random.uniform(-200, 200))

        return Vector2D(x, y)

    def filtrePerception(self):
        l = []

        return l

    def update(self):

        inf = AnimateAction(None, None, None)
        inf.move = self.moveRandom()
        if inf.move.x < inf.move.y :
            inf.move.x=0
        else:
            inf.move.y=0
        return inf

