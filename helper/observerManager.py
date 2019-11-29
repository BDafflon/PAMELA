import csv
from csv import *


class ObserverManager:
    def __init__(self, pathDir):
        self.observer = []
        self.pathDir = pathDir

    def addObservation(self, o):
        self.observer.append(o)

    def removeObserver(self, o):
        self.observer.remove(o)

    def write(self):
        fileTaxi = open(self.pathDir+"/taxi.csv", "w")
        fileClient = open(self.pathDir + "/client.csv", "w")

        try:
            writerTaxi = csv.writer(fileTaxi, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writerClient = csv.writer(fileClient, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #Client: id, idTaxi, heure de commande, heure de prise en charge, temps de trajet, distance de trajet, temps de marche, distance de marche

            #Taxi: id, heure du deplacement, distance, nombre de passagers.
            writerTaxi.writerow(["id Taxi", "id deplacement", "heure de départ (s)","distance(m)", "temps de deplacement(s)","nombre de passager"])
            writerClient.writerow(["id Client","id Taxi","heure de commande(s)","heure de prise en charge(s)","temps de trajet(s)","distance theorique(m)","distance de trajet(m)","distance de marche(m)","temps de marche(s)"])

            #
            # Écriture des quelques données.

            for l in self.observer:
                if l.type=="Taxi":
                    writerTaxi.writerow([l.id,l.idDeplacement,l.HDepart,l.distance,l.temps,l.nbPassager])
                else:
                    writerClient.writerow([l.id,l.idTaxi,l.HCommande,l.HPriseEnCharge,l.tempsTrajet,l.distanceTheorique,l.distance,l.distanceMarche,l.tempsMarche])
        finally:
            #
            # Fermeture du fichier source
            #
            fileTaxi.close()
            fileClient.close()
