import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper.util import signedAngle, toOrientationVector, randomInt
from helper.vector2D import Vector2D


class Boid(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille=1
        self.body.mass = 80
        self.body.fustrum.radius = 50
        self.body.vitesseMax=1
        self.repultion = 50
        self.attraction=1

    def __init__(self,f):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 50
        self.body.vitesseMax = 1
        self.repultion = 50
        self.attraction= 1

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)



    def filtrePerception(self):
        l = []


        return l

    def update(self):
        influence = AnimateAction(None, Vector2D(0,0),0)
        l = []

        for a in self.body.fustrum.perceptionList:
            if a.type == "Boid":
                if a.famille == self.famille:
                    l.append(a)


        influence.rotatoin = self.align(l)
        m=self.cohesion(l)
        m = m.scale(self.attraction)


        influence.move = m

        m = self.separation(l)
        m=m.scale(self.repultion)

        influence.move.x =  influence.move.x + m.x
        influence.move.y = influence.move.y + m.y
        return influence

    def align(self, boids):
        angleAlign = 0



        if len(boids) > 0:
            angle=0
            vOrientation = toOrientationVector(self.body.orientation)
            for b in boids:
                angle=angle+signedAngle(vOrientation,toOrientationVector(b.body.orientation))

            angle=angle/len(boids)
            angleAlign=angle
        else:
            angleAlign = 0
        return angleAlign

    def cohesion(self, boids):
        steering = Vector2D(0,0)

        if len(boids) > 0:
            center = Vector2D(0,0)
            for b in boids:

                center.x=center.x+b.body.location.x
                center.y = center.y + b.body.location.y

            center.x = center.x / len(boids)
            center.y = center.y / len(boids)

            dest = Vector2D(0,0)
            dest.x= center.x - self.body.location.x
            dest.y= center.y - self.body.location.y

            steering = dest
        return steering




    def separation(self, boids):
        steering = Vector2D(0,0)

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
            steering=rep
        return steering