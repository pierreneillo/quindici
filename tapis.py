from cartes_paquet import *
import itertools

__about__ = """Module tapis.py: Implémente la classe tapis, qui représente l'endroit où sont posées les cartes"""

class Tapis:
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
        @position: un str dans la chaîne 'SONE'
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
        self.quindici = False#On remet quinidici à False, et on le passera à True s'il y a un quindici
        combinaisons_possibles = []
        for i in range(1, len(self.contenu)+1):
            combinaisons_possibles.extend(list(itertools.combinations(self.contenu,i)))#liste des toutes les combinaisons possibles, pas mnécessairement de 15 points
        combinaisons_possibles = [combinaison for combinaison in combinaisons_possibles if sum([x.valeur for x in combinaison])==15]
        #on "élague", pour ne garder que les combinaisons de 15 points
        combinaisons_possibles.sort(key=len, reverse=True)
        #on trie la liste par nombre de cartes, car plus il y a de cartes, plus la combinaison est intéressante
        if len(combinaisons_possibles)!=0:#Si il y a des combinaisons de 15 points, il y a quindici
            self.quindici = True#on passe donc quindici à True
            combinaison_max_cartes = [combinaisons_possibles[0]]#on sélectionne la combinaison avec le plus de cartes
            max = len(combinaisons_possibles[0])#Longueur maximale de combinaison trouvée
            for i in range(len(combinaisons_possibles)):#On vérifie si il n'y a pas d'autres combinaisons de cartes du même nombre de cartes
                if len(combinaisons_possibles[i])==max:
                    combinaison_max_cartes.append(combinaisons_possibles[i])
                else:
                    break
            combinaison_max_cartes.sort(key = lambda x:len([y for y in x if y.couleur == 'd']))#on trie les combinaisons ayant un nombre maximal de cartes par nombre de carreaux
            combinaison_optimale = combinaison_max_cartes[-1]#Et la combinaison optimale est celle qui en a le plus.
            #TODO: Affiner pour prendre en compte les 7 aussi, et pour mettre un pénalité si on laisse une combinaison à l'adversaire
            if len(combinaison_optimale) == len(self.contenu):
                self.scopa = True#Si on a pris toutes les cartes du tapis, il y a scopa
            else:
                self.scopa = False#Sinon, non
        else:#Si la longueur de combinaisons possibles est de 0, il n'y a pas quindici
            combinaison_optimale = []
        return self.quindici, combinaison_optimale


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
