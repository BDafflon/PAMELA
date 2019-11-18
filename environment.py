import util
import random
from taxi import Taxi
from object import Destination
from animateAction import AnimateAction
import time
from client import Client
from vector2D import Vector2D
import threading
import ctypes


class Environment(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.boardW = 1000
        self.boardH = 1000
        self.running = 1

        self.agents = []
        self.objects = []
        self.perceptionList = {}
        self.influenceList = {}

    def addAgent(self, a):
        self.agents.append(a)

    def addObject(self, o):
        self.objects.append(o)

    def getRandomObject(self, typeO):
        while True:
            d = util.randomInt(len(self.objects))
            if self.objects[d].type == typeO:
                return self.objects[d]

    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                if a.stat == 1:
                    if a.onboard == -1:
                        return a
        return None

    def run(self):
        try:

            while self.running == 1:

                time.sleep(0.002)
                self.perceptionList = {}
                self.influenceList = {}

                for agent in self.agents:

                    self.checkStat(agent)
                for agent in self.agents:
                    self.computePerception(agent)

                for agent in self.agents:

                    self.influenceList[agent.id] = None
                    self.influenceList[agent.id] = agent.update()

                self.applyInfluence()

        finally:
            print('ended')

    def checkStat(self, a):

        if a.stat == -1:
            self.agents.remove(a)

        if isinstance(a, Client):

            if a.stat == 0:
                a.addDestination(self.getRandomObject("Destination"))

        if isinstance(a, Taxi):

            if a.stat == 0:

                d = self.getRandomAgent("Client")

                if not d == None:
                    a.addClient(d)

    def computePerception(self, a):
        self.perceptionList[a] = []
        for agent in self.agents:
            if agent != a:
                if a.body.insidePerception(agent.body.location, agent.type):
                    self.perceptionList[a].append(agent)
        for objet in self.objects:
            if a.body.insidePerception(objet.location, agent.type):
                self.perceptionList[a].append(objet)

        a.body.fustrum.perceptionList = self.perceptionList[a]

    def applyInfluence(self):
        actionList = {}
        for k, influence in self.influenceList.items():
            agentBody = self.getAgentBody(k)

            if not agentBody is None:

                move = Vector2D(influence.x, influence.y)
                rotation = 0
                move = agentBody.computeMove(move)
                move=move.scale(0.2)
                agentBody.move(move)

    def getAgentBody(self, k):
        for a in self.agents:
            if a.id == k:
                return a.body
        return None

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
