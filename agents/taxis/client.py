import random
import time

from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper import util
from helper.observer import ClientObserver
from helper.policy import ClientsPolicy
from helper.vector2D import Vector2D
from environment.object import Destination


class Client(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.destination = Destination(0, 0)
        self.onboard = -1
        self.type = "Client"
        self.body.mass = 80
        self.body.vitesseMax = 1
        self.body.fustrum.radius = 100
        self.policy = ClientsPolicy.COHESION
        self.observer = ClientObserver(self.id, time.time(),self.body.location)
        self.cohesionFactor = 0.03
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def addDestination(self, d):
        self.destination = d
        self.stat = 1
        self.observer.HCommande = time.time()
        self.observer.distanceTheorique = d.location.distance(self.body.location)
        print(self.observer.distanceTheorique)

    def filtrePerception(self):
        l = []
        for a in self.body.fustrum.perceptionList:
            if isinstance(a, Client):
                if a.destination.location == self.destination.location:
                    l.append(a)
        return l

    def update(self):

        influence = AnimateAction(None, None, None)
        influence.move = Vector2D(0, 0)

        # kill me
        if self.stat == 2:
            self.stat = -1
            return influence

        if self.onboard == 1:
            return influence
        else:
            if self.destination.location.distance(self.body.location) < 2:
                self.stat = 2

        if self.stat == 0:
            influence.move = self.moveRandom()

        if self.stat == 1:
            l = self.filtrePerception()
            influence.move = Vector2D(0.0, 0.0)

            if len(l) > 0:
                if self.policy == ClientsPolicy.COHESION:
                    c = self.average_position(l)
                    self.velocity[0] = c.x * self.cohesionFactor
                    self.velocity[1] = c.y * self.cohesionFactor

                    self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
                    influence.move = Vector2D(self.velocity[0], self.velocity[1])
                    self.observer.update(self.body.location)
                    self.body.velocity = influence.move

        return influence

    def average_position(self, nearby_clients):

        if len(nearby_clients) > 0:

            sum = Vector2D(0.0, 0.0)
            for c in nearby_clients:
                sum.x += c.body.location.x
                sum.y += c.body.location.y

            average = Vector2D((sum.x / len(nearby_clients)), (sum.y / len(nearby_clients)))

            return average
        else:
            return Vector2D(0.0, 0.0)
