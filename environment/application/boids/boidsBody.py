from environment.body import Body


class BoidsBody(Body):
    def __init__(self):
        Body.__init__(self)
        self.collistionDistance = 45.0
        self.obstacleCollisionDistance = 250
        self.maxCollisionVel = 1.0
