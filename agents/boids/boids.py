import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from environment.application.boids.boidsBody import BoidsBody
from helper import util
from helper.vector2D import Vector2D


class Boid(Agent):
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
        self.repultion = 150
        self.cohesionFactor = 0.03
        self.collisionDistance = 10
        self.velocity = random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)
        self.allignFactor = 0.045
        self.avoidanceFactor = 7.5
        self.attractorFactor = 0.0035
        self.obstacleFactor = 200

    def __init__(self, f):
        Agent.__init__(self)
        self.body = BoidsBody()
        self.type = "Boid"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 100
        self.body.vitesseMax = 150.0
        self.body.vitesseMin = 20.0
        self.repultion = 150
        self.collisionDistance = 45.0
        self.collisionDVel = 1
        self.cohesionFactor = 0.03
        self.velocity = [random.uniform(-50.0, 50.0), random.uniform(-50.0, 50.0)]
        self.allignFactor = 0.045
        self.avoidanceFactor = 2.5
        self.attractorFactor = 0.35
        self.obstacleFactor = 200

    def moveRandom(self):
        x = int(random.uniform(-2, 2))
        y = int(random.uniform(-2, 2))

        return Vector2D(x, y)

    def filtrePerception(self):
        l = []
        other = []
        target = []
        for b in self.body.fustrum.perceptionList:
            if b.type == self.type:
                if b.famille == self.famille:
                    l.append(b)
                else:
                    other.append(b)
            elif b.type == "Attractor":
                target.append(b)
        return l,other,target

    def update(self):

        inf = AnimateAction(None, None, None)
        nearby_boids,other_b, attractors = self.filtrePerception()
        cohesion_vector = self.average_position(nearby_boids)
        alignment_vector = self.average_velocity(nearby_boids)
        attractor_vector = self.attraction(attractors)
        boid_avoidance_vector = self.avoid_collisions(nearby_boids)
        obstacle_avoidance_vector = self.avoid_collisions(other_b)

        self.change_vectors = [
            (self.cohesionFactor, cohesion_vector),
            (self.allignFactor, alignment_vector),
            (self.attractorFactor, attractor_vector),
            (self.avoidanceFactor, boid_avoidance_vector),
            (self.obstacleFactor, obstacle_avoidance_vector)]

        for factor, vec in self.change_vectors:
            self.velocity[0] += factor * vec[0]
            self.velocity[1] += factor * vec[1]


        self.velocity = util.limit_magnitude(self.velocity, self.body.vitesseMax, self.body.vitesseMin)
        inf.move = Vector2D(self.velocity[0], self.velocity[1])
        self.body.velocity = inf.move
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
        return util.limit_magnitude(c, self.body.maxCollisionVel)

    def attraction(self, attractors):
        # generate a vector that moves the boid towards the attractors
        a = [0.0, 0.0]

        for attractor in attractors:
            a[0] += attractor.location.x - self.body.location.x
            a[1] += attractor.location.y - self.body.location.y

        return a

