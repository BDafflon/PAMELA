import util
import random
from vector2D import Vector2D
from fustrum import CircularFustrum

class Body:
	def __init__(self):
		self.id = util.id_generator(10,"1234567890")
		self.mass=1
		self.location = Vector2D(util.randomInt(1000),util.randomInt(1000))
		self.fustrum = CircularFustrum(20)
		self.orientation = 0
		self.vitesseMax = 1
		self.accelerationMax=1
		
	def insidePerception(self,p,t):
		return self.fustrum.inside(self.location,p)	

	def computeMove(self,v):
		 
		m = Vector2D(v.x, v.y)
		 
		if(m.getLength()<=0):
			m = Vector2D(0,0)	
			return m
		 
		if m.getLength() > self.vitesseMax :
			m=m.getNormalized()
			m.scale(self.vitesseMax)
			 
		return m	

	def move(self,v):
		self.location.x= self.location.x+v.x
		self.location.y= self.location.y+v.y
	 
		 
