from environment.environment import Environment
from helper import util
from agents.taxis.taxi import Taxi
import time
from agents.taxis.client import Client
from helper.vector2D import Vector2D
import threading
import ctypes


class EnvironmentBoids(Environment):
    def __init__(self):
        Environment.__init__(self)



    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                        return a
        return None


    def run(self):
        try:

            while self.running == 1:

                time.sleep(0.0002)
                self.perceptionList = {}
                self.influenceList = {}

                for agent in self.agents:
                    self.computePerception(agent)

                for agent in self.agents:
                    self.influenceList[agent.id] = None
                    self.influenceList[agent.id] = agent.update()

                self.applyInfluence()

        finally:
            print('ended')


