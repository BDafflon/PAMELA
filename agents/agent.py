import random

from helper import util
from environment.body import Body


class Agent:
    def __init__(self):
        self.velocity = random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)
        self.id = util.id_generator(10, "123456789")
        self.type = "Agent"
        self.body = Body()
        self.stat = 0

    def update(self):
        print(self.id)
        print(len(self.body.fustrum.perceptionList))
