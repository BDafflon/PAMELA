from environment.environment import Environment
from agents.taxis.taxi import Taxi
from agents.taxis.client import Client
from helper.vector2D import Vector2D


class EnvironmentTaxis(Environment):
    def __init__(self):
        Environment.__init__(self)

    def getFirstTaxi(self):
        return self.getRandomAgent("Taxi")

    def update(self, dt):

        self.perceptionList = {}
        self.influenceList = {}

        for agent in self.agents:
            self.checkStat(agent)

        for agent in self.agents:
            self.computePerception(agent)

        for agent in self.agents:
            self.influenceList[agent.id] = None
            self.influenceList[agent.id] = agent.update()

        self.applyInfluence(dt)

    def checkStat(self, a):
        if a.stat == -1:
            self.agents.remove(a)

        if isinstance(a, Client):
            if a.stat == 0:
                a.addDestination(self.getRandomObject("Destination"))

        if isinstance(a, Taxi):
            if a.stat == 0:
                d = self.getRandomAgent("Client")

                if d is not None:
                    a.addClient(d)

    def applyInfluence(self, dt):

        for k, influence in self.influenceList.items():

            if influence is None:
                continue

            agentBody = self.getAgentBody(k)

            if agentBody is not None:
                move = Vector2D(influence.move.x, influence.move.y)
                rotation = 0
                move = agentBody.computeMove(move)
                move = move.scale(dt)
                agentBody.move(move)
