from helper.vector2D import Vector2D


class AnimateAction:
	def __init__(self):
		self.body = None
		self.move=Vector2D(0,0)
		self.rotatoin = 0

	def __init__(self,b,m,r):
		self.body = b
		self.move=m
		self.rotatoin = r		 
