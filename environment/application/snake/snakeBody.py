from environment.body import Body
from helper.util import signedAngle
from helper.vector2D import Vector2D


class SnakeBody(Body):
    def __init__(self):
        Body.__init__(self)
        self.tail = []
        self.tail.append(Vector2D(self.location.x + 1, self.location.y))
        self.tail.append(Vector2D(self.location.x + 2, self.location.y))
        self.tail.append(Vector2D(self.location.x + 3, self.location.y))

    def growup(self, v):
        self.tail.append(v)

    def move(self, v):
        a = signedAngle(self.velocity, v)
        if a is None:
            self.velocity = v
            return
        print("a " + str(a))
        if abs(a) >= 3:
            return
        for i in range(0, len(self.tail) - 1):
            print(str(self.tail[len(self.tail) - 1 - i]) + "=" + str(self.tail[len(self.tail) - 2 - i]))
            self.tail[len(self.tail) - 1 - i] = self.tail[len(self.tail) - 2 - i]

        self.tail[0] = self.location

        v = v.getNormalized()

        self.location.x = self.location.x + v.x
        self.location.y = self.location.y + v.y
        self.velocity = v
