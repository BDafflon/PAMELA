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
        self.environment = EnvironmentTaxis()
        self.path = path
        self.ready = False
        self.obsManager=ObserverManager("./res")
        self.scheduling=[]
        self.factor=10000

    def loadScenario(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            center = Vector2D(0,0)
            upLeft = Vector2D(0,0)
            downRight = Vector2D(0,0)
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    event = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7])]
                    if line_count==1:
                            upLeft.x = event[1]
                            upLeft.y = event[2]
                            downRight.x = event[1]
                            downRight.y = event[2]


                    self.scheduling.append(event)
                    center.x = center.x+event[1]
                    center.y = center.y+ event[2]

                    if upLeft.x > event[1]:
                        upLeft.x = event[1]
                    if upLeft.y > event[2]:
                        upLeft.y = event[2]

                    if downRight.x < event[1]:
                        downRight.x = event[1]
                    if downRight.y < event[2]:
                        downRight.y = event[2]

                    print(f'\t{event[0]} s ;  [{event[1]},{event[2]}] to [{event[3]},{event[4]}] - {event[7]} passagers.')
                    line_count += 1

            center.x=(center.x/line_count)
            center.y=(center.y/line_count)

            print("c: "+center.toString()+ " upLeft :"+upLeft.toString()+" downRight :"+downRight.toString())
            self.environment.center=center
            self.environment.boardW =(downRight.x - upLeft.x)*self.factor
            self.environment.boardH = (downRight.y - upLeft.y)* self.factor
            print(self.environment.boardW)
            print(self.environment.boardH)
            self.ready = True

    def loadDestination(self):
        self.environment.addObject(Destination(10, 10))
        self.environment.addObject(Destination(490, 10))
        self.environment.addObject(Destination(10, 490))
        self.environment.addObject(Destination(490, 490))
        self.environment.addObject(Destination(255, 255))

    def loadTaxi(self,n):
        for i in range(0,n):
            t = Taxi(self.obsManager)
            self.environment.addAgent(t)

    def loadDefault(self):
        for i in range(1, 6):
            c= Client()
            self.environment.addAgent(c)
            self.obsManager.addObservation(c.observer)
        self.ready = True


    def run(self):
        if self.ready:
            print("START")
            iterator = 0;
            startTime = int(time.time())
            while iterator < len(self.scheduling):
                elapseTime = int(time.time()) - startTime
                if elapseTime>self.scheduling[iterator][0]:
                    iterator = iterator + 1
                    for i in range(0,int(self.scheduling[iterator][7])):
                        a = Client()
                        x=self.environment.boardW/2+self.scheduling[iterator][1] + self.environment.center.x
                        y=self.environment.boardH/2+self.scheduling[iterator][2] + self.environment.center.x

                        a.body.location=Vector2D(x,y)
                        print("start agent "+ a.body.location.toString())
                        self.environment.addAgent(a)
                        self.obsManager.addObservation(a.observer)


        else:
            print("Erreur de simulation")
