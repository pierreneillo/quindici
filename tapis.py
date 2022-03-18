import random
from cartes_paquet import Carte, PaquetCartes
import itertools

def affiche_jeu(liste_cartes):
    for carte in liste_cartes:
        print(carte, end = '+')
    print()


## c'est le tapis où les joueurs posent une carte chacun leur tour
class Tapis():
    def __init__(self):
        '''
        @contenu : liste d'objets cartes
        @joueur_actuel : str dans la chaîne SN : indique qui pose sa carte sur le tapis
        @quindici : Booléen indiquant s'il existe une (ou plusieurs) combinaisons valant 15
        @scopa : Booléen indiquant si la combinaison trouvée permet de vider le tapis
        '''
        self.contenu = []
        self.quindici = False
        self.scopa = False
        self.joueur_actuel = ''

    def est_vide(self):
        pass



    def changer_joueur(self, position):
        '''
        position est un str dans la chaîne 'SONE'
        '''
        pass

    def afficher(self):
        if self.est_vide():
            print("tapis vide")
        else:
            print("tapis : ", end = ' ')
            #à compléter : faites afficher toutes les cartes du tapis
            # (en ligne de préférence)
            #exemple :  tapis :  s3 🂣+sJ 🂫+s1 🂡+d3 🃃+
            #
            #..........
            #

        print() #pour sauter une ligne



    def ajouter(self, carte):
        '''ajoute la carte au contenu du tapis'''
        pass



    def enlever(self, id_carte):
        '''
        enlève la carte de la liste contenu et la renvoie
        id_carte est un str du type 'c7'
        si on ne trouve pas la carte, on lève une exception type ValueError
        '''
        pass



    def tester_quindici(self):
        '''
        c'est la "grosse méthode" du tapis
        renvoie un tuple avec :
        - Un booléen indiquant s'il existe une combinaison de cartes qui vaut 15
        - et une liste, soit vide, soit contenant les cartes de la combinaison optimale
        S'il y a plusieurs combinaisons valant 15... On prend celle avec le plus de cartes
        et à égalité : celle où il y a le plus de carreaux
        (on pourrait aussi traiter à part le 7 de carreaux...)
        '''
        #à vous


        return quindici, combinaison_optimale


#test
if __name__ == '__main__':

    #créer des objets de type Carte
    carte1=........

    l = [carte1, carte2, carte3, carte4, ...]
    #tester les méthodes de votre classe tapis en regardant les différents cas


