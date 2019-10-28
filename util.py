import string
import random
from vector2D import Vector2D

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
	
