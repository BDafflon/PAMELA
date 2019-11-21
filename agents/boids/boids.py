import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper.util import signedAngle, toOrientationVector
from helper.vector2D import Vector2D
from environment.object import Destination


class Boid(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille=1
        self.body.mass = 80
        self.body.fustrum.radius = 10

    def __init__(self,f):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 10

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)



    def filtrePerception(self):
        l = []


        return l

    def update(self):

        influence = Vector2D(0, 0)


        return influence

    def align(self, boids):
        steering = AnimateAction()
        total = 0


        if len(boids) > 0:
            angle=0
            vOrientation = toOrientationVector(self.body.orientation)
            for b in boids:
                angle=angle+signedAngle(vOrientation,toOrientationVector(b.body.orientation))

            angle=angle/len(boids)
            steering.rotatoin=angle
        else:
            steering.rotatoin = 0
        return steering

    def cohesion(self, boids):
        steering = AnimateAction()
        return steering

    def separation(self, boids):
        steering = AnimateAction()
        return steering
