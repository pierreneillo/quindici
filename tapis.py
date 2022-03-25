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
        return len(self.contenu)==0



    def changer_joueur(self, position):
        '''
        position est un str dans la chaîne 'SONE'
        '''
        self.joueur_actuel = position

    def afficher(self):
        if self.est_vide():
            print("tapis vide")
        else:
            print("tapis : ", end = ' ')
            repr_cartes = list(map(repr,self.contenu)))
            print(" + ".join(repr_cartes))

        print() #pour sauter une ligne



    def ajouter(self, carte):
        '''ajoute la carte au contenu du tapis'''
        self.contenu.append(carte)



    def enlever(self, id_carte):
        '''
        enlève la carte de la liste contenu et la renvoie
        id_carte est un str du type 'c7'
        si on ne trouve pas la carte, on lève une exception type ValueError
        '''
        #First check if card is on the table:
        id_contenu = list(map(lambda x:x.couleur+x.hauteur,self.contenu))
        if id_carte not in id_contenu:
            raise ValueError("La carte n'est pas sur le tapis")
        self.contenu.pop(id_contenu.index(id_carte))
            



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
        #TODO: comment all the code of this method
        quindici = False
        combinaisons_possibles = []
        for i in range(1, len(self.contenu)+1):
            combinaisons_possibles.extend(list(itetools.combinations(self.contenu),i))
        combinaisons_possibles = [combinaison for combinaison in combinaison_possibles if sum(combinaison, key = lambda x:x.valeur)==15]
        combinaisons_possibles.sort(key=len)
        if len(combinaisons_possibles)!=0:
            quindici = True
            combinaisons_min_cartes = [combinaisons_possibles[0]]
            min = len(combinaisons_possibles[0])
            for i in range(len(combinaisons_possibles)):
                if len(combinaisons_possibles[i])==min:
                    combinaisons_min_cartes.append(combinaisons_possibles[i])
                else:
                    break
            combinaisons_min_cartes.sort(key = lambda x:len([y for y in x if y.couleur == 's']))
            combinaison_optimale = combinaisons_min_cartes[-1]
        else:
            combinaison_optimale = None
        return quindici, combinaison_optimale


#test
if __name__ == '__main__':

    #créer des objets de type Carte
    carte1=........

    l = [carte1, carte2, carte3, carte4, ...]
    #tester les méthodes de votre classe tapis en regardant les différents cas


