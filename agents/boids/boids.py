import random
from agents.agent import Agent
from environment.animateAction import AnimateAction
from helper.util import signedAngle, toOrientationVector, randomInt
from helper.vector2D import Vector2D

_COHESION_FACTOR = 0.03
_ALIGNMENT_FACTOR = 0.045
_BOID_AVOIDANCE_FACTOR = 7.5
_OBSTACLE_AVOIDANCE_FACTOR = 300.0
_ATTRACTOR_FACTOR = 0.0035


class Boid(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille = 1
        self.body.mass = 80
        self.body.fustrum.radius = 200
        self.body.vitesseMax = 1
        self.repultion = 150
        self.attraction = 1
        self.collisionDistance = 10

    def __init__(self, f):
        Agent.__init__(self)
        self.type = "Boid"
        self.famille = f
        self.body.mass = 80
        self.body.fustrum.radius = 200
        self.body.vitesseMax = 1
        self.repultion = 150
        self.attraction = 1
        self.collisionDistance = 45

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
        influence = AnimateAction(None, Vector2D(0, 0), 0)
        l = self.filtrePerception()

        cohesion_vector = self.average_position(l)
        alignment_vector = self.average_velocity(l)
        # attractor_vector = self.attraction(attractors)
        boid_avoidance_vector = self.avoid_collisions(l)

        cohesion_vector = cohesion_vector.scale(_COHESION_FACTOR)
        alignment_vector = alignment_vector.scale(_ALIGNMENT_FACTOR)
        boid_avoidance_vector = boid_avoidance_vector.scale(_OBSTACLE_AVOIDANCE_FACTOR)

        influence.move = Vector2D(0, 0)
        influence.move = influence.move.add(cohesion_vector)
        influence.move = influence.move.add(alignment_vector)
        influence.move = influence.move.add(boid_avoidance_vector)

        if influence.move.getLength() > self.body.vitesseMax:
            influence.move = influence.move.getNormalized()
            influence.move = influence.move.scale(self.body.vitesseMax)
        return influence

    def average_position(self, nearby_boids):
        # take the average position of all nearby boids, and move the boid towards that point
        if len(nearby_boids) > 0:
            sumPos = Vector2D(0, 0)
            for boid in nearby_boids:
                sumPos.x += boid.body.location.x
                sumPos.y += boid.body.location.y

            average = Vector2D(0, 0)
            average.x = (sumPos.x / len(nearby_boids))
            average.y = sumPos.y / len(nearby_boids)

            vec = Vector2D(0, 0)
            vec.x = average.x - self.body.location.x
            vec.y = average.y - self.body.location.y

            return vec
        else:
            return Vector2D(0, 0)

    def average_velocity(self, nearby_boids):
        # take the average velocity of all nearby boids
        # todo - combine this function with average_position
        if len(nearby_boids) > 0:
            sumVel = Vector2D(0, 0)
            for boid in nearby_boids:
                sumVel.x += boid.body.velocity.x
                sumVel.y += boid.body.velocity.y

            average = Vector2D(0, 0)
            average.x = (sumVel.x / len(nearby_boids))
            average.y = sumVel.y / len(nearby_boids)

            vec = Vector2D(0, 0)
            vec.x = average.x - self.body.velocity.x
            vec.y = average.y - self.body.velocity.y

            return vec
        else:
            return Vector2D(0, 0)

    def avoid_collisions(self, l):
        # determine nearby objs using distance only

        c = Vector2D(0, 0)
        for obj in l:
            diff = Vector2D(0, 0)
            diff = Vector2D(obj.body.location.x - self.body.location.x, obj.body.location.y - self.body.location.y)
            if diff.lengthSquared() == 0 :
                continue
            inv_sqr_magnitude = 1 / diff.lengthSquared()

            c.x = c.x - inv_sqr_magnitude * diff.x
            c.y = c.y - inv_sqr_magnitude * diff.y

        vec = Vector2D(c.x, c.y)
        if vec.getLength() > self.collisionDistance:
            vec = vec.getNormalized()
            vec = vec.scale(self.collisionDistance)
        return vec
