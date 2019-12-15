import csv
import threading
import time

from agents.taxis.client import Client
from agents.taxis.taxi import Taxi
from environment.application.taxis.environmentTaxis import EnvironmentTaxis
from environment.object import Destination
from helper.observerManager import ObserverManager
from helper.vector2D import Vector2D


class SimulationTaxis(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.limitSimulation = 6000
        self.environment = EnvironmentTaxis()
        self.path = path
        self.ready = False
        self.obsManager = ObserverManager("./res")
        self.scheduling = []
        self.factor = 10
        self.nbTaxi = 25
        self.center = Vector2D(0, 0)
        self.upLeft = Vector2D(0, 0)
        self.downRight = Vector2D(0, 0)
        self.Gui = None

    def loadScenario(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            center = Vector2D(0, 0)

            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    event = [float(row[0]), float(row[1]) / self.factor, float(row[2]) / self.factor,
                             float(row[3]) / self.factor, float(row[4]) / self.factor, float(row[5]), float(row[6]),
                             float(row[7])]

                    self.scheduling.append(event)
                    self.center.x = self.center.x + event[1]
                    self.center.y = self.center.y + event[2]
                    line_count += 1

            self.center.x = (self.center.x / line_count)
            self.center.y = (self.center.y / line_count)

            self.environment.center = self.center
            self.upLeft = Vector2D(0, 0)
            self.downRight = Vector2D(0, 0)

            if len(self.scheduling) >= 1:
                self.upLeft.x = self.scheduling[0][1]
                self.upLeft.y = self.scheduling[0][2]
                self.downRight.x = self.scheduling[0][1]
                self.downRight.y = self.scheduling[0][2]

            for event in self.scheduling:
                event[1] = event[1]
                event[2] = event[2]
                print(f'\t{event[0]} s ;  [{event[1]},{event[2]}] to [{event[3]},{event[4]}] - {event[7]} passagers.')
                if self.upLeft.x > event[1]:
                    self.upLeft.x = event[1]
                if self.upLeft.y > event[2]:
                    self.upLeft.y = event[2]

                if self.downRight.x < event[1]:
                    self.downRight.x = event[1]
                if self.downRight.y < event[2]:
                    self.downRight.y = event[2]

            print(
                "c: " + self.center.toString() + " upLeft :" + self.upLeft.toString() + " downRight :" + self.downRight.toString())

            self.environment.boardW = (self.downRight.x - self.upLeft.x)
            self.environment.boardH = (self.downRight.y - self.upLeft.y)
            print(self.environment.boardW)
            print(self.environment.boardH)
            self.ready = True

    def loadDestination(self):
        x = (self.downRight.x + self.upLeft.x) / 2
        y = (self.downRight.y + self.upLeft.y) / 2
        self.environment.addObject(Destination(x - self.center.x + self.environment.boardW / 2,
                                               y - self.center.y + self.environment.boardH / 2))
        '''self.environment.addObject(Destination(self.downRight.x-self.center.x+self.environment.boardW/2, self.upLeft.y-self.center.y+self.environment.boardH/2))
        self.environment.addObject(Destination(self.upLeft.x -self.center.x+self.environment.boardW/2, self.downRight.y-self.center.y+self.environment.boardH/2))
        self.environment.addObject(Destination(self.downRight.x-self.center.x+self.environment.boardW/2, self.downRight.y-self.center.y+self.environment.boardH/2))
        self.environment.addObject(Destination(self.upLeft.x-self.center.x+self.environment.boardW/2, self.upLeft.y-self.center.y+self.environment.boardH/2))
'''

    def loadTaxi(self):
        x = (self.downRight.x + self.upLeft.x) / 2
        y = (self.downRight.y + self.upLeft.y) / 2
        for i in range(0, self.nbTaxi):
            t = Taxi(self.obsManager)
            t.body.location = Vector2D(x - self.center.x + self.environment.boardW / 2,
                                       y - self.center.y + self.environment.boardH / 2)
            print("Taxi :" + t.body.location.toString())
            self.environment.addAgent(t)

    def loadDefault(self):
        for i in range(1, 6):
            c = Client()
            self.environment.addAgent(c)
            self.obsManager.addObservation(c.observer)
        self.ready = True

    def run(self):
        if self.ready:
            print("START")
            iterator = 0;
            startTime = int(time.time())
            while iterator < len(self.scheduling) - 1:
                elapseTime = int(time.time()) - startTime
                if elapseTime > self.limitSimulation:
                    break

                if elapseTime > self.scheduling[iterator][0]:
                    iterator = iterator + 1
                    for i in range(0, int(self.scheduling[iterator][7])):
                        d = self.environment.getRandomObject("Destination")
                        a = Client()
                        a.addDestination(d)
                        x = self.scheduling[iterator][1] - self.environment.center.x + self.environment.boardW / 2
                        y = self.scheduling[iterator][2] - self.environment.center.y + self.environment.boardH / 2

                        a.body.location = Vector2D(x, y)
                        print(
                            "start agent " + str(iterator) + "/" + str(len(self.scheduling)) + " t:" + str(elapseTime))
                        self.environment.addAgent(a)
                        self.obsManager.addObservation(a.observer)
            print("Fin de simulation")
            self.Gui.stop2()


        else:
            print("Erreur de simulation")
