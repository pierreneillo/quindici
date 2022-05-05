import random
from constantes import *

__about__ = """Module cartes_paquet.py: implémente les classes Carte et PaquetCartes, servant respectivement à représenter une carte de jeu et un paquet de cartes"""


class Carte:
    """
    Classe représentant une carte de jeu
    """
    #on récupère les dessins Unicode des cartes (sauf le cavalier)
    JEU_IMAGES = [[chr(127184 - c*16 + h + 1 + (h > 12)) for h in range(13)] for c in range(4)]

    def __init__(self, couleur, hauteur):
        '''
        @hauteur est un str de '1' pour l'As à 'K' pour le roi
        @couleur est un str entre 'c', 'd', 'h', 's'
        @valeur est un entier correspondant à la force de la carte
         : 1 pour la plus faible (1) à 10 pour le Roi
        @dessin est un caractère Unicode représentant la carte en miniature
        @id est un str composé de la couleur de la carte et de sa hauteur
        @valeur2 est un flottant égal à la valeur de l carte -0.1 si la carte est carreau égal à la valeur de la carte sinon; utile pour l'IA
        '''
        self.couleur = couleur
        self.hauteur = hauteur
        self.dessin = self.JEU_IMAGES[DICO_COULEURS[couleur]][DICO_HAUTEURS_SCOPA[hauteur]]
        self.valeur = DICO_VALEURS[hauteur]
        self.id=self.couleur+self.hauteur #on concatène les attributs couleur et hauteur
        if self.couleur=='d':
            self.valeur2=float(self.valeur)-0.1
        else:
            self.valeur2=self.valeur

    def __str__(self):
        return self.couleur+self.hauteur + ' ' + self.dessin
    
    def __repr__(self):
        return self.couleur+self.hauteur + ' ' + self.dessin


class PaquetCartes:
    """Représente le paquet de carte utilisé pour le jeu"""
    def __init__(self, nb):
        '''
        @nb_cartes: le nombre de cartes dans le paquet
        @cartes: Un tableau dynamique python contenant des instances de la classe Carte, représente le paquet de cartes
        '''
        self.nb_cartes = nb
        if nb!=40:
            raise ValueError(VALUE_ERROR)
            """
            hauteur_min = 0 if nb == 52 else 6 #on commence au 7 pour un jeu de 32
            self.cartes = [Carte(couleur, hauteur) for hauteur in HAUTEURS[hauteur_min:] for couleur in COULEURS]
            if nb ==32:
                #il faut rajouter l'As
                self.cartes.extend([Carte(couleur, '1') for couleur in COULEURS])
            """
        if nb == 40:
            #Jeu de scopa
            self.cartes = [Carte(couleur, hauteur) for hauteur in HAUTEURS_SCOPA for couleur in COULEURS]


    def battre(self):
        '''
        mélange le paquet de façon aléatoire
        '''
        random.shuffle(self.cartes)#Mélange la liste en place

    def couper(self):
        '''
        Simule le fait de couper le paquet en deux à un endroit aléatoire
        puis de permuter les deux parties "dessus - dessous"
        '''
        i_coupe = random.randint(0,len(self.cartes)-1)
        dessous = self.cartes[:i_coupe]
        dessus = self.cartes[i_coupe:]
        self.cartes = dessus + dessous

    def est_vide(self):
        '''
        Renvoie un booléen, qui représente le fait que le paquet de cartes soit vide
        '''
        return len(self.cartes)==0

    def remplir(self, cartes):
        '''
        @cartes est une liste d'objets Carte
        Cette méthode ajoute les cartes en question au paquet
        '''
        #Dans la deuxième condition, on teste si tous les éléments de la liste sont de la classe Carte.
        #Pour cela, on crée une chaîne de caractères composée de 1 et de 0, ou chaque 1 représente un élément
        #qui est effectivement de la classe Carte et chaque 0 représente un élément qui n'est pas de la classe Carte.
        #On compare ensuite cette chaîne à '1'*len(cartes)
        if type(cartes)==list and "".join([str(int(type(e)==Carte)) for e in cartes])=='1'*len(cartes):
            self.cartes.extend(cartes)
        else:
            raise ValueError("'cartes' doit être une liste d'éléments de type Carte'")

    def tirer(self):
        '''
        renvoie la carte tirée au sommet du paquet
        si le paquet est vide, lève une exception
        '''
        if self.est_vide():
            raise IndexError("Stack is empty")
        else:
            return self.cartes.pop()


def affiche_jeu(liste_cartes):
    """Affiche toutes les cartes du jeu de cartes passé en argument"""
    return " ".join(list(map(str,liste_cartes)))

#tests : quand vous êtes prêt

if __name__ == '__main__':
    paq = PaquetCartes(32)
    paq.battre()
    for i in range(7):
        c = paq.tirer()
        print(c)
    print(paq.est_vide())
