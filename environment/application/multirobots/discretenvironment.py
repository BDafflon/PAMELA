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
        self.map[a.body.location.x][a.body.location.y].append(a)

    def applyInfluence(self, dt):
        actionList = {}
        for k, influence in self.influenceList.items():

            if influence == None:
                continue

            agentBody = self.getAgentBody(k)

            if not agentBody is None:
                move = Vector2D(influence.move.x, influence.move.y)
                rotation = 0
                move = agentBody.computeMove(move)
                move = move.scale(dt)
                #DETECTION DE COLLISION ?

                #MOVE
                a = self.getAgent(k)
                self.map[a.body.location.x][a.body.location.y].remove(a)
                agentBody.move(move)
                self.edges(agentBody)
                self.map[a.body.location.x][a.body.location.y].append(a)