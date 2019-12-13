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
        self.body.vitesseMax = 100
        self.body.fustrum.radius = 100
        self.policy = ClientsPolicy.COHESION
        self.observer = ClientObserver(self.id, time.time(),self.body.location)
        self.cohesionFactor = 0.03
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.allignFactor = 0.045

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def moveTo(self, d):
        return Vector2D(d[0] - self.body.location.x,
                        d[1] - self.body.location.y)

    def addDestination(self, d):
        self.destination = d
        self.stat = 1
        self.observer.HCommande = time.time()
        self.observer.distanceTheorique = d.location.distance(self.body.location)
        print(self.id)


    def filtrePerception(self):
        l = []
        for a in self.body.fustrum.perceptionList:
            if a.type=="Client":
                if a.onboard != 1:
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
                return influence

        if self.stat == 0:
            influence.move = self.moveRandom()

        if self.stat == 1:
            nearby_client = self.filtrePerception()
            influence.move = Vector2D(0.0, 0.0)

            if len(nearby_client) > 0:
                if self.policy == ClientsPolicy.COHESION:
                    cohesion_vector = self.average_position(nearby_client)
                    alignment_vector = self.average_velocity(nearby_client)

                    influence.move = self.moveTo(cohesion_vector)
                    self.observer.updateMarche(self.body.location)

        self.body.velocity = influence.move
        return influence

    def average_position(self, nearly_clients):
        if len(nearly_clients) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearly_clients:
                sum_x += boid.body.location.x
                sum_y += boid.body.location.y

            average_x, average_y = (sum_x / len(nearly_clients), sum_y / len(nearly_clients))
            return [average_x - self.body.velocity.x, average_y - self.body.velocity.y]
        else:
            return [0.0, 0.0]

    def average_velocity(self, nearly_clients):

        if len(nearly_clients) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearly_clients:
                sum_x += boid.body.velocity.x
                sum_y += boid.body.velocity.y

            average_x, average_y = (sum_x / len(nearly_clients), sum_y / len(nearly_clients))

            return [average_x - self.body.velocity.x, average_y - self.body.velocity.y]
        else:
            return [0.0, 0.0]