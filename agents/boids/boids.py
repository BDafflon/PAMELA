import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper import util
from helper.util import signedAngle, toOrientationVector, randomInt
from helper.vector2D import Vector2D


_BOID_COLLISION_DISTANCE = 45.0
_OBSTACLE_COLLISION_DISTANCE = 250.0
_MAX_COLLISION_VELOCITY = 1.0


_COHESION_FACTOR = 0.03
_ALIGNMENT_FACTOR = 0.045
_BOID_AVOIDANCE_FACTOR = 7.5
_OBSTACLE_AVOIDANCE_FACTOR = 200
_ATTRACTOR_FACTOR = 0.0035


class Boid(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.collisionDVel = 1
        self.type = "Boid"
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 250
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.repultion = 150
        self.attraction = 1
        self.collisionDistance = 10
        self.velocity=random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)

    def __init__(self, f):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 200
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.repultion = 150
        self.attraction = 1
        self.collisionDistance = 45.0
        self.collisionDVel = 1
        self.velocity=[random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def filtrePerception(self):
        l = []

        for b in self.body.fustrum.perceptionList:
            if b.type == self.type:
                if b.famille == self.famille:
                    l.append(b)
        return l

    def update(self):

        inf = AnimateAction(None,None,None)
        nearby_boids= self.filtrePerception()
        cohesion_vector = self.average_position(nearby_boids)
        alignment_vector = self.average_velocity(nearby_boids)
        attractor_vector = [0,0]
        boid_avoidance_vector = self.avoid_collisions(nearby_boids)
        obstacle_avoidance_vector = [0,0]

        self.change_vectors = [
                                  (_COHESION_FACTOR, cohesion_vector),
                                  (_ALIGNMENT_FACTOR, alignment_vector),
                                  (_ATTRACTOR_FACTOR, attractor_vector),
                                  (_BOID_AVOIDANCE_FACTOR, boid_avoidance_vector),
                                  (_OBSTACLE_AVOIDANCE_FACTOR, obstacle_avoidance_vector)]

        for factor, vec in self.change_vectors:
            self.velocity[0] += factor * vec[0]
            self.velocity[1] += factor * vec[1]

        # ensure that the boid's velocity is <= _MAX_SPEED
        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        inf.move = Vector2D(self.velocity[0],self.velocity[1])
        self.body.velocity =inf.move
        return inf

    def average_position(self, nearby_boids):

        if len(nearby_boids) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearby_boids:
                sum_x += boid.body.location.x
                sum_y += boid.body.location.y

            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [average_x - self.body.location.x, average_y - self.body.location.y]
        else:
            return [0.0, 0.0]

    def average_velocity(self, nearby_boids):

        if len(nearby_boids) > 0:
            sum_x, sum_y = 0.0, 0.0
            for boid in nearby_boids:
                sum_x += boid.body.velocity.x
                sum_y += boid.body.velocity.y

            average_x, average_y = (sum_x / len(nearby_boids), sum_y / len(nearby_boids))
            return [average_x - self.body.velocity.x, average_y - self.body.velocity.y]
        else:
            return [0.0, 0.0]

    def avoid_collisions(self, objs):
        # determine nearby objs using distance only

        c = [0.0, 0.0]
        for obj in objs:
            diff = obj.body.velocity.x - self.body.location.x, obj.body.velocity.y - self.body.location.y
            inv_sqr_magnitude = 1 / ((util.magnitude(*diff) - 10) ** 2)

            c[0] = c[0] - inv_sqr_magnitude * diff[0]
            c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return util.limit_magnitude(c, _MAX_COLLISION_VELOCITY)
