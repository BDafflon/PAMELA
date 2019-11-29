from helper import util
from helper.vector2D import Vector2D


class Observer:
    def __init__(self, id, type):
        self.id=id
        self.type=type
        self.dernierePosition = Vector2D(0, 0)

    def update(self, location):
        self.distance=self.distance+abs(self.dernierePosition.distance(location))

        if self.type =="Client":
            print("--" + str(self.distance))
        self.dernierePosition = Vector2D(location)



class TaxiObserver(Observer):
    def __init__(self,id,h):
        Observer.__init__(self,id,"Taxi")
        self.idDeplacement = ""
        self.HDepart = h
        self.distance = 0.0
        self.temps=h
        self.nbPassager=0

class ClientObserver(Observer):
    def __init__(self,id,h):
        Observer.__init__(self,id,"Client")
        self.idTaxi = ""
        self.HCommande = h
        self.HPriseEnCharge = 0.0
        self.tempsTrajet = 0.0
        self.distanceTheorique = 0.0
        self.distance=0.0
        self.distanceMarche=0.0
        self.tempsMarche=0.0


