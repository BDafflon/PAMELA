from environment.environment import Environment
import time

from helper.vector2D import Vector2D


class EnvironmentBoids(Environment):
    def __init__(self):
        Environment.__init__(self)

    def getRandomAgent(self, typeO):
        for a in self.agents:
            if a.type == typeO:
                return a
        return None

    def getFirstBoid(self):
        return self.getRandomAgent("Boid")

    def update(self, dt):
        self.clock = (time.time())

        self.influenceList = {}

        for agent in self.agents:
            self.computePerception(agent)

        for agent in self.agents:
            self.influenceList[agent.id] = None
            self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)
        #print("dt : " + str(dt))

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
                move = move.scale(dt*100)
                agentBody.move(move)
                self.edges(agentBody)
