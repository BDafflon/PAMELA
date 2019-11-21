import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper.util import signedAngle, toOrientationVector, randomInt
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

        influence = AnimateAction()
        l = []
        for a in self.body.fustrum.perceptionList:
            if a.type == "Boid":
                if a.famille == self.famille:
                    l.append(a)


        influence.rotatoin = self.align(l).rotatoin
        influence.move = self.cohesion(l).move
        influence.move.x =  influence.move.x + self.separation().move.x
        influence.move.y = influence.move.y + self.separation().move.y
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

        if len(boids) > 0:
            center = Vector2D(0,0)
            for b in boids:

                center.x=center.x+b.body.location.x
                center.y = center.y + b.body.location.y

            center.x = center.x / len(boids)
            center.y = center.y / len(boids)

            dest = Vector2D(0,0)
            dest.x=self.body.location.x - center.x
            dest.y=self.body.location.y - center.y
            steering.move = dest
            return steering




    def separation(self, boids):
        steering = AnimateAction()

        if len(boids) > 0:
            tmp = Vector2D(0, 0)
            rep = Vector2D(0, 0)
            for b in boids:
                tmp.x = self.body.location.x- b.body.location.x
                tmp.y = self.body.location.y- b.body.location.y

                if tmp.getLength() == 0:
                     tmp =  Vector2D(randomInt(1), randomInt(1))
                tmp = tmp.scale(1/(tmp.lengthSquared()))

                rep=rep.add(tmp)
            steering.move=rep
        return steering