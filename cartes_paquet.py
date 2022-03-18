import random
from constantes import *


class Carte:
    #variables de classe : correspondance hauteurs et couleurs
    #on récupère les dessins Unicode des cartes (sauf le cavalier)
    JEU_IMAGES = [[chr(127184 - c*16 + h + 1 + (h > 12)) for h in range(13)] for c in range(4)]

    def __init__(self, couleur, hauteur):
        '''
        @hauteur est un str de '1' pour l'As à 'K' pour le roi
        @couleur est un str entre 'c', 'd', 'h', 's'
        @valeur est un entier correspondant à la force de la carte
         : 2 pour la plus faible (2) à 14 pour l'As (le plus fort)
        @dessin est un caractère Unicode représentant la carte en miniature
        '''
        self.couleur = couleur
        self.hauteur = hauteur
        self.dessin = self.JEU_IMAGES[DICO_COULEURS[couleur]][DICO_HAUTEURS[hauteur]]
        #à compléter
        self.valeur = DICO_VALEURS[hauteur]

    def __str__(self):
        #permet de faire print facilement
        return self.couleur+self.hauteur + ' ' + self.dessin


class PaquetCartes:
    def __init__(self, nb):
        self.nb_cartes = nb
        if nb!=40:
            hauteur_min = 0 if nb == 52 else 6 #on commence au 7 pour un jeu de 32
            self.cartes = [Carte(couleur, hauteur) for hauteur in HAUTEURS[hauteur_min:]
                                           for couleur in COULEURS]
        if nb ==32:
            #il faut rajouter l'As
            self.cartes.extend([Carte(couleur, '1') for couleur in COULEURS])
        if nb == 40:
            #Jeu de scopa
            self.cartes = [Carte(couleur, hauteur) for hauteur in HAUTEURS_SCOPA for couleur in COULEURS]


    def battre(self):
        '''
        mélange le paquet de façon aléatoire
        '''
        random.shuffle(self.cartes)

    def couper(self):
        '''
        simule le fait de couper le paquet en deux à un endroit aléatoire
        puis de permuter les deux parties "dessus - dessous"
        '''
        i_coupe = random.randint(0,len(self.cartes)-1)
        dessous = self.cartes[:i_coupe]
        dessus = self.cartes[i_coupe:]
        self.cartes = dessus + dessous

    def est_vide(self):
        return len(self.cartes)==0

    def remplir(self, cartes):
        '''
        cartes est une liste d'objets Carte
        cette méthode ajoute les cartes en question au paquet
        '''
        #Dans la deuxième condition, on teste si tous les éléments de la liste sont de la classe Carte.
        #Pour cela, on crée une chaîne de caractères composée de 1 et de 0, ou chaque 1 représente un élément qui est effectivement de la classe Carte et chaque 0 représente un élément qui n'est pas de la classe Carte.
        #On compare ensuite cette chaîne à la représentation binaire de 2**(len(cartes+1) - 1 soit '1'*len(cartes)
        if type(cartes)==list and "".join([str(int(type(e)==Carte)) for e in cartes])==bin((1<<len(cartes)+1)-1)[2:]:
            self.cartes.extend(cartes)
        else:
            raise ValueError("'cartes' doit être une liste d'éléments de type Carte'")

    def tirer(self):
        '''
        renvoie la carte tirée au sommet du paquet
        si le paquet est vide, lève une exception
        '''
        pass


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
