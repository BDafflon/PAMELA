import util
import random
from point2D import Point2D
from fustrum import CircularFustrum

class AnimateAction:
	def __init__(self):
		self.body = None
		self.move=Point2D(0,0)
		self.rotatoin = 0

	def __init__(self,b,m,r):
		self.body = b
		self.move=m
		self.rotatoin = r		 
