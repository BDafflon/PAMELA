import util
import random
from agent import Agent 
from vector2D import Vector2D
from client import Client

class Taxi(Agent):
    
    
	def __init__(self):
		Agent.__init__(self)
		self.capacity = 5
		self.occupation = 0
		self.type = "Taxi"
		self.body.mass=1000
		self.stat=0
		self.clients = []
		self.body.fustrum.radius=20
	 

	def addClient(self,c):
		 
		if c in self.clients :
			 
		else :		
			if self.capacity - self.occupation >0 :
				self.clients.append(c)
				self.stat=1
				c.onboard=0
				self.occupation=self.occupation+1
				 
			 

	def removeClient(self,c):
		self.clients.remove(c)
		self.occupation=self.occupation-1
		c.onboard=0
		c.body.location=Vector2D(self.body.location.x,self.body.location.y)

	def moveRandom(self):
		x =int(random.uniform(-2,2))
		y =int(random.uniform(-2,2))

		return Vector2D(x,y)
	


	def moveTo(self,d):
		return Vector2D(d.location.x-self.body.location.x,d.location.y-self.body.location.y)


	def hasClient(self):
		i=0
		for c in self.clients:
			if c.onboard == 0 :
				i=i+1
		return i

	def hasClientOn(self):
		for c in self.clients:
			if c.onboard == 1 :
				return c
		return None	

	def filtreClient(self,cl):
		l=[]
		
		
		for a in self.body.fustrum.perceptionList:
			 
			if isinstance(a,Client):
				 
				if a.stat==1:
					 
					if a.onboard == -1:
						 
						if a.destination.location == cl.destination.location :
							 
							if self.capacity - self.occupation >0 :							
								self.addClient(a)
								l.append(a)
				
		return l
		
	def waitingClient(self,clients):
		l=[]
		for c in self.clients:
			if c.onboard == 0 :
				l.append(c)
		return l
							
	def update(self): 
		 
		influence = Vector2D(0,0)

		if len(self.clients)==0:
			influence = self.moveRandom()
		else:
			
			cl = self.clients[0]
			
			
			l=self.filtreClient(cl)
		 

			

			for c in self.clients:
				if c.body.location.distance(self.body.location) < 2 :
						c.onboard=1
				if c.destination.location.distance(self.body.location) < 2  :	
					if cl.onboard==1:
						self.removeClient(cl)	
			
			 

			i = self.hasClient()
			
			if i>0 :
				influence = self.moveTo(util.getNextByDistance(self.body.location,self.waitingClient(self.clients)))
			else :
				
				influence = self.moveTo(cl.destination)	
		 
				

	
					
		
		if len(self.clients)==0:
			self.stat=0
		 
 		return influence

