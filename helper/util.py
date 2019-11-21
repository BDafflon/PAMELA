import string
import random
import math
from helper.vector2D import Vector2D

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def randomInt(m):
	return int(random.uniform(0, m))

def getNextByDistance(source,destinations):
	v = Vector2D(0,0)
	mini= 100000000
	for d in destinations:
		if source.distance(d.body.location) < mini :
			mini = source.distance(d.body.location)
			v = d
	return v.body


def signedAngle(v1,v2):
	a = Vector2D(v1.x,v1.y)
	if a.getLength() == 0:
		return None

	b = Vector2D(v2.x,v2.y)
	if b.getLength() == 0:
		return None

	a = a.getNormalized()
	b= b.getNormalized()

	cos = a.x * b.x + a.y * b.y;
	sin = a.x * b.y - a.y * b.x;
	angle = math.atan2(sin, cos);
	return angle;

def toOrientationVector(angle):
		return Vector2D( math.cos(angle), math.sin(angle));

