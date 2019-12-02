from environment.environment import Environment
import time
from helper.vector2D import Vector2D


class DiscretEnvironment(Environment):
    def __init__(self):
        Environment.__init__(self)
        self.map=[]


    def createMap(self):
        for i in range(0,self.boardW):
            self.map.append([])
            for j in range(0,self.boardH):
                self.map[i].append([])


    def addAgent(self, a):
        self.agents.append(a)
        self.map[a.body.location.x][a.body.location.y]=a