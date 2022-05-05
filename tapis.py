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

    def __repr__(self):
        if self.est_vide():
            s="Tapis vide"
        else:
            s="Tapis : "
            repr_cartes = list(map(repr,self.contenu))
            s+=" + ".join(repr_cartes)
        return s



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
        Cette méthode actualise l'attribut scopa
        '''
        self.quindici = False#On remet self.quindici à False
        combinaisons_possibles = []#Listes des combinaisons possibles avec les cartes du tapis, pas forcément de 15 points.
        for i in range(1, len(self.contenu)+1):
            combinaisons_possibles.extend(list(itertools.combinations(self.contenu,i)))
            #On utilise itertools pour former toutes les combinaisons possibles de i cartes,
            #Avec celles du tapis (itertools.combinations renvoie des tuples contenant toutes les combinaisons possibles
            #Avec le premier argument, dont la longueur est i, autrement dit ici tous les
            #Arrangements de i cartes parmi celles de self.contenu
        combinaisons_possibles = [combinaison for combinaison in combinaisons_possibles if sum([x.valeur for x in combinaison])==15]
        #On ne garde que celles dont la longueur est 15
        combinaisons_possibles.sort(key=len, reverse=True)
        #On les trie par longueur, de la plus grande à la plus petite
        if len(combinaisons_possibles)!=0:#Si il y a des combinaisons de 15 possibles
            self.quindici = True#Il y a quindici => On le signale
            combinaison_max_cartes = [combinaisons_possibles[0]]#On regarde si plusieurs combinaisons ont la même longueur que la plus longue
            max = len(combinaisons_possibles[0])
            for i in range(len(combinaisons_possibles)):
                if len(combinaisons_possibles[i])==max:
                    combinaison_max_cartes.append(combinaisons_possibles[i])
                else:
                    break
            combinaison_max_cartes.sort(key = lambda x:len([y for y in x if y.couleur == 'd']))
            combinaison_optimale = combinaison_max_cartes[-1]
            #On trie la liste des combinaisons sélectionnées par nombre de carreaux, et on sélectionne la meilleure
            #On notera ici qu'on ne prend pas en compte les 7
            if len(combinaison_optimale) == len(self.contenu):
                self.scopa = True#On vérifie si il y a scopa
            else:
                self.scopa = False
        else:
            combinaison_optimale = []#Si il n'y a aucune combinaison possible de cartes ont la somme des points fait 15
            #On remplace combinaison_optimale par une liste vide
        return self.quindici, combinaison_optimale#On renvoie le tout


#test
if __name__ == '__main__':
    def tester(texte):
        print(texte)
        print(tapis)
        print(tapis.tester_quindici())
        print("Scopa :",tapis.scopa)
        print()

    #créer des objets de type Carte
    l = [Carte('s','J'), Carte('h','3'), Carte('d','5'), Carte('c','4')]
    tapis = Tapis()
    tester("Cas classique#0: paquet vide")
    for c in l:
        tapis.ajouter(c)

    tester("Cas classique#1: Une seule combinaison possible")

    tapis.enlever('sJ')
    tester("Cas classique#2: Aucune combinaison possible")

    tapis.ajouter(Carte('s','J'))
    tapis.enlever('d5')
    tester("Cas classique#3: 1 scopa possible")

    tapis.ajouter(Carte('s','7'))
    tester("Cas Intermédiaire#4: Comparer 2 combinaisons possibles dont le nombre de cartes diffère")

    tapis.enlever('s7')
    tapis.ajouter(Carte('d','4'))
    tapis.ajouter(Carte('d','3'))
    tester("Cas intermédaire#5: Comparer plusieurs combinaisons possibles dont le nombre de carreaux diffère mais dont le nombre de cartes est le même")
