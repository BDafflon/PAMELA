import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.boids.boidsBody import BoidsBody
from helper import util
from helper.vector2D import Vector2D


class StandardAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.body = BoidsBody()
        self.collisionDVel = 1
        self.type = "Boid"
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.avoidanceFactor = 7.5
        self.obstacleFactor = 500
        self.target = Vector2D(0,0)

    def __init__(self, f):
        Agent.__init__(self)
        self.body = BoidsBody()
        self.type = "StandardAgent"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.avoidanceFactor = 7.5
        self.obstacleFactor = 500
        self.target = Vector2D(0, 0)

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def filtrePerception(self):
        l = []
        other = []
        target = []

        return l, other, target

    def update(self):
        inf = AnimateAction(None, None, None)
        nearby_boids, other_b, attractors = self.filtrePerception()

        boid_avoidance_vector = self.avoid_collisions(nearby_boids)
        obstacle_avoidance_vector = self.avoid_collisions(other_b)



        self.change_vectors = [

            (self.avoidanceFactor, boid_avoidance_vector),
            (self.obstacleFactor, obstacle_avoidance_vector)]

        for factor, vec in self.change_vectors:
            self.velocity[0] += factor * vec[0]
            self.velocity[1] += factor * vec[1]

        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move
        return inf

    def avoid_collisions(self, objs):
        # determine nearby objs using distance only

        c = [0.0, 0.0]
        for obj in objs:
            diff = obj.body.velocity.x - self.body.location.x, obj.body.velocity.y - self.body.location.y
            inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

            c[0] = c[0] - inv_sqr_magnitude * diff[0]
            c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return util.limit_magnitude(c, self.body.maxCollisionVel)
