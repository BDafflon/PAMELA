import time
from environment.animateAction import AnimateAction
from helper import util
import random
from agents.agent import Agent
from helper.observer import TaxiObserver
from helper.policy import TaxisPolicy
from helper.vector2D import Vector2D
from agents.taxis.client import Client



class Taxi(Agent):
    def __init__(self,obs):
        Agent.__init__(self)
        self.capacity = 5
        self.occupation = 0
        self.type = "Taxi"
        self.body.mass = 1000
        self.stat = 0
        self.clients = []
        self.body.fustrum.radius = 200
        self.observerM = obs
        self.observer = None
        self.policy = TaxisPolicy.MAXPASSAGER

    def addClient(self, c):
        if not c in self.clients:
            if self.capacity - self.occupation > 0:
                self.clients.append(c)
                self.stat = 1
                c.onboard = 0
                self.occupation = self.occupation + 1

    def removeClient(self, c):
        self.clients.remove(c)
        self.occupation = self.occupation - 1
        c.onboard = 0
        c.body.location = Vector2D(self.body.location.x, self.body.location.y)

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))
        return Vector2D(x, y)

    def moveTo(self, d):

        return Vector2D(d.location.x - self.body.location.x,
                        d.location.y - self.body.location.y)

    def hasClient(self):
        i = 0
        for c in self.clients:
            if c.onboard == 0:
                i = i + 1
        return i

    def hasClientOn(self):
        i=0
        for c in self.clients:
            if c.onboard == 1:
               i=i+1
        return i

    def filtreClient(self, cl):
        l = []

        for a in self.body.fustrum.perceptionList:

            if isinstance(a, Client):

                if a.stat == 1:

                    if a.onboard == -1:

                        if a.destination.location == cl.destination.location:

                            if self.capacity - self.occupation > 0:
                                self.addClient(a)
                                l.append(a)

        return l

    def waitingClient(self, clients):
        l = []
        for c in self.clients:
            if c.onboard == 0:
                l.append(c)
        return l

    def update(self):
        self.updateObs()
        influence = AnimateAction(None, None, None)

        if len(self.clients) == 0:
            influence.move = self.moveRandom()
        else:

            cl = self.clients[0]

            if self.policy == TaxisPolicy.MAXPASSAGER :
                l = self.filtreClient(cl)

            for c in self.clients:

                if c.onboard == 1:
                    c.body.location=self.body.location


                if c.body.location.distance(self.body.location) < 2:
                    c.onboard = 1

                    c.observer.HPriseEnCharge=time.time()
                    c.observer.idTaxi=self.id
                    c.observer.update(self.body.location)
                    c.observer.distance = 0

                if c.destination.location.distance(self.body.location) < 2:
                    if cl.onboard == 1:

                        self.removeClient(cl)
                        c.observer.tempsTrajet = time.time()-c.observer.HPriseEnCharge

            i = self.hasClient()

            if i > 0:
                influence.move = self.moveTo(
                    util.getNextByDistance(self.body.location,
                                           self.waitingClient(self.clients)))
            else:

                influence.move = self.moveTo(cl.destination)

        if len(self.clients) == 0:
            self.stat = 0
        self.body.velocity = influence.move
        return influence

    def updateObs(self):
        if self.observer is None:
            self.observer = TaxiObserver(self.id, time.time())
            self.observer.idDeplacement = util.id_generator(10, "123456789")
            self.observer.nbPassager = 0
            self.observer.update(self.body.location)
            self.observer.distance = 0
        else:

            if self.observer.nbPassager != self.hasClientOn():
                self.observer.temps = time.time() - self.observer.HDepart
                self.observerM.addObservation(self.observer)
                if self.hasClientOn()==0:
                    self.observer = None
                else:
                    t= self.observer.idDeplacement
                    p = self.hasClientOn()
                    self.observer = TaxiObserver(self.id,time.time())
                    self.observer.idDeplacement = t
                    self.observer.nbPassager = p
                    self.observer.update(self.body.location)
                    self.observer.distance = 0
            else:
                self.observer.update(self.body.location)


