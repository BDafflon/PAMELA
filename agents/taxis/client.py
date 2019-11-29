import random
from agents.agent import Agent
from helper.vector2D import Vector2D
from environment.object import Destination


class Client(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.destination = Destination(0, 0)
        self.onboard = -1
        self.type = "Client"
        self.body.mass = 80
        self.body.fustrum.radius = 10

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def addDestination(self, d):
        self.destination = d
        self.stat = 1

    def filtrePerception(self):
        l = []
        for a in self.body.fustrum.perceptionList:
            if isinstance(a, Client):
                if a.destination.location == self.destination.location:
                    l.append(a)
        return l

    def update(self):
        influence = Vector2D(0, 0)
        if self.onboard == 1:
            return influence
        else:
            if self.destination.location.distance(self.body.location) < 5:
                self.stat = 2
        if self.stat == 0:
            influence = self.moveRandom()
        if self.stat == 1:
            l = self.filtrePerception()

            for c in l:
                vect = Vector2D(0, 0)
                vect = c.body.location.sub(self.body.location)
                influence = influence.add(vect)

        return influence
