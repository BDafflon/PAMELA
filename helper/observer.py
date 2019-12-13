from helper import util
from helper.vector2D import Vector2D


class Observer:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.dernierePosition = Vector2D(0, 0)

    def update(self, location):
        self.distance = self.distance + abs(self.dernierePosition.distance(location))
        self.dernierePosition = Vector2D(location)


class TaxiObserver(Observer):
    def __init__(self, id, h):
        Observer.__init__(self, id, "Taxi")
        self.idDeplacement = ""
        self.HDepart = h
        self.distance = 0.0
        self.temps = h
        self.nbPassager = 0


class ClientObserver(Observer):
    def __init__(self, id, h, location):
        Observer.__init__(self, id, "Client")
        self.idTaxi = ""
        self.HCommande = h
        self.HPriseEnCharge = 0.0
        self.tempsTrajet = 0.0
        self.distanceTheorique = 0.0
        self.distance = 0.0
        self.distanceMarche = 0.0
        self.tempsMarche = 0.0
        self.dernierePositionM = None

    def updateMarche(self, location):
        if self.dernierePositionM is None:
            self.dernierePositionM = location
            self.distanceMarche =0
        else:
            self.distanceMarche = self.distanceMarche + abs(self.dernierePositionM.distance(location))
            self.dernierePositionM = Vector2D(location)
