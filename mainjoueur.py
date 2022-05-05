from cartes_paquet import *
from tapis import *


class MainJoueur:
    """décrit le joueur et son jeu, contient sa position (Nord=ordi sud=joueur)"""

    def __init__(self,cartes,position):
        """
        @cartes: est un tableau dynamique composé de plusieurs objets Carte représentant la main du joueur
        @position: est un str parmi 'S' ou 'N'
        @plis: tableau dynamique contenant les Cartes remportées par le joueur
        @nb_scopa: int comptant les points obtenus par scopa
        """
        #on vérifie que les variables rentrées correspondent à ce qui est attendu
        assert type(cartes) is list,'cartes doit être un tableau dynamique'
        for carte in cartes:
            assert type(carte) is Carte,"cartes doit être un tableau d'objets Carte"
        assert position=='S' or position=="N","position vaut 'S' pour le joueur 'N' pour l'ordinateur"
        self.cartes=cartes
        self.position=position
        self.plis=[]
        self.nb_scopa=0


    #méthodes
    def est_vide(self):
        """Renvoie True si la main cartes est vide false sinon"""
        return self.cartes==[] or self.cartes is None

    def trier_main(self):
        '''trie l'attribut cartes par ordre croissant de valeur des cartes'''
        self.cartes.sort(key=lambda carte:carte.valeur)


    def afficher(self):
        """affiche le jeu trié par valeur de cartes"""
        if self.est_vide():
            print('la main est vide')
        else:
            reponse=''
            self.trier_main()

            for i in range(len(self.cartes)):
                reponse+=str(self.cartes[i])
                if i!=len(self.cartes)-1:
                    reponse+='-'

            print(reponse)


    def recevoir(self,carte):
        """prend en paramètre une carte et l'insère dans le jeu"""
        assert type(carte)==Carte,"carte n'est pas un objet de type Carte"
        self.cartes.append(carte)


    def rejeter(self,id_carte):
        """prend en paramètre l'identifiant d'une carte
        supprime la carte du paquet cartes
        renvoie la carte supprimée"""
        #on vérifie que la carte est présente dans le paquet
        present=False

        for carte in self.cartes:
            if carte.id.lower()==id_carte.lower():
                present=True
                supprimee=carte
        assert present,'la carte cherchée n\'est pas dans le paquet'
        #on la supprime du paquet
        self.cartes.remove(supprimee)

        return supprimee


    def ajoute_plis(self,plis):
        """ajoute le plis rentré en paramètre dans le plis du joueur"""
        #on vérifie que plis en paramètre est un tableau de cartes
        assert type(plis)==list,"plis est un tableau "
        for carte in plis:
            assert type(carte) is Carte,"les éléments de plis sont des Cartes"

        #on ajoute le plis au plis du joueur
        self.plis+=plis


    def choix_output(self):
        """récupère le choix du joueur par input texte(= str id_cartes), si le joueur fait une erreur on recommence (pas indéfinimment grâce à l'ajout d'un compteur) """
        present=False
        compteur=0
        while not(present) and compteur!=5:
            compteur+=1
            id_carte=input('saisissez l\'identifiant de la carte : ').lower()

            #on vérifie que la carte est présente dans le paquet
            for carte in self.cartes:
                #print(carte.id.lower(),id_carte)
                if carte.id.lower()==id_carte:
                    present=True
                    choisie=carte
        if compteur==5:
            print('Vous passez votre tour : vous auriez dû vous concentrer et saisir le bon id')
        elif present:
            return choisie
    def ecu_7():
        return len([True for carte in self.cartes if carte.id.lower()=="d7"])


class MainJoueurIA(MainJoueur):
    """décrit le jeu de l'IA et toutes ses actions possibles"""
    def __init__(self,cartes,position='N'):
        super().__init__(cartes,position)



    def score_v1(self,carte):
        '''quantifie l'intérêt de jouer la carte en paramètre,renvoie un nombre entre 0 et 1 '''
        #vouée à évoluer en score(self,carte,tapis)
        assert type(carte)==Carte,"l'objet en paramètre est une Carte"


        if carte.valeur>7:
            if carte.couleur=='d':#carte est J,Q,K de carreau (intéressante à jouer car carreau raporte un point à la fin mais comme la valeur est grande on a moins de possibilité de vider le tapis)
                score=0.25

            else:#carte est J,G,K de trèfle, pique, coeur : valeur trop grande et rapporte aucun point à la fin donc 0
                score=0



        elif carte.valeur<7:
            if carte.couleur=='d':#carte est 1,2,3,4,5,6 de carreau : valeur petite, pour avoir une somme de 15 on va ramasser plus de cartes=>chance importante de vider tapis + 1 point à la fin car carreau
                score=0.75


            else:#1,2,3,4,5,6 de trèfle coeur et pique (on va pouvoir ramasser beaucoup de cartes voire vider le tapis)
                score=0.5

        else:#carte.valeur==7
            if carte.couleur=='d':#carte est 7 de carreaux : très intéressant à jouer car rapporte 1+1 point à la fin
                score=1
            else:#carte est 7 de trèfle coeur pique
                score=0.76


        return score


    def choix_output(self,tapis):
        """Choisit quelle carte jouer pour l'IA
        @param:
          - @tapis: le tapis en cours
        Renvoie une carte, celle à jouer pour obtenir le plus de points possibles"""
        #Vérification de la validité du contexte
        if len(self.cartes)==0:
            raise IndexError("La main de l'IA est vide")
        if type(tapis)!=Tapis:
            raise ValueError("L'objet en paramètre n'est pas un Tapis")
        #On commence par créer un nouvel objet Tapis, le duplicata de celui passé en paramètre, qu'on pourra modifier à notre guise
        tapis_modif = Tapis()
        tapis_modif.contenu = tapis.contenu[:]
        meilleure_carte = self.cartes[0]
        combi_meilleure_carte = None
        for carte in self.cartes:
            #On ajoute successivement chaque carte au tapis et on regarde quelle est la meilleure combinaison
            tapis_modif.ajouter(carte)
            quindici,combinaison_optimale = tapis_modif.tester_quindici()
            #La qualité du jeu de l'IA dépend uniquement de la fonction comparer
            if quindici and self.comparer(combi_meilleure_carte,combinaison_optimale):
                combi_meilleure_carte = combinaison_optimale
                meilleure_carte = carte
            tapis_modif.enlever(carte.id)
        if combi_meilleure_carte is None:
            cartes_triees=sorted(self.cartes,key = lambda x: self.score_v1(x))
            return cartes_triees[0]
        else:
            return meilleure_carte

    def comparer(self,combi1,combi2):
        """Compare deux combinaisons et renvoie True si la deuxième est meilleure que la première, False sinon
        @param:
          - @combi1: combinaison de cartes
          - @combi2: combinaison de cartes"""
        #print("combi1=",combi1)
        #print("combi2=",combi2)
        if combi1 is None: return True
        if combi2 == []: return False
        if len(combi1)!=len(combi2):
            if combi1[-1] in self.cartes:
                print(f"score de {combi1[-1]}={len(combi1)}")
            if combi2[-1] in self.cartes:
                print(f"score de {combi2[-1]}={len(combi2)}")
            return len(combi1)<len(combi2)
        #On calcule le nombre de carreaux dans chaque combinaison
        nb_carreaux_1=len([carte for carte in combi1 if carte.couleur=="d"])
        nb_carreaux_2=len([carte for carte in combi2 if carte.couleur=="d"])
        #On calcule le nombre de septs dans chaque combinaison
        nb_septs_1=len([carte for carte in combi1 if carte.hauteur=="7"])
        nb_septs_2=len([carte for carte in combi2 if carte.hauteur=="7"])
        #On calcule le score de chaque combinaison en fonction de ces deux critères
        score_1 = 0.2*nb_carreaux_1+0.8*nb_septs_1
        score_2 = 0.2*nb_carreaux_2+0.8*nb_septs_2
        if combi1[-1] in self.cartes:
            print(f"score de {combi1[-1]}={score_1}")
        if combi2[-1] in self.cartes:
            print(f"score de {combi2[-1]}={score_2}")
        return score_1 < score_2









#tests
if __name__=='__main__':


    #tests MainJoueur
    print('*****Début des tests pour MainJoueur*****\n')
    #tests constructeur
    j1=MainJoueur([Carte('c','Q'),Carte('d','5'),Carte('h','1')],'S')
    j2=MainJoueur([],'N')
    assert not(j1.est_vide())#est_vide() ok
    assert j2.est_vide()
    j1.afficher()#afficher ok
    j2.afficher()
    print("+++++afficher ok+++++")
    j1.recevoir(Carte('d','4'))#recevoir ok
    j2.recevoir(Carte('d','2'))
    j1.afficher()
    j2.afficher()
    print("+++++recevoir ok+++++")
    j1.rejeter('h1')#rejeter ok
    j2.rejeter('d2')
    j1.afficher()
    j2.afficher()
    print("+++++rejeter ok+++++")
    print(j1.plis)
    print(j2.plis)
    j1.ajoute_plis(PaquetCartes(40).cartes)#ajoute_plis ok
    j2.ajoute_plis(PaquetCartes(40).cartes)
    print(j1.plis)
    print(j2.plis)
    print("+++++ajoute_plis ok+++++")
    j1.afficher()
    print('test choix output',j1.choix_output())
    j1.afficher()
    print("+++++choix_output ok+++++")




    #tests MainJoueurIA
    print()
    print('*****Début des tests pour MainJoueurIA*****\n')
    print('-----Première version score_v1(carte) et choix_output()-----')
    j3=MainJoueurIA([Carte('h','Q'),Carte('s','7'),Carte('d','1')],'N')
    #print(j3.choix_output())
    assert j3.score_v1(Carte('h','Q'))==0
    assert j3.score_v1(Carte('d','7'))==1
    assert j3.score_v1(Carte('c','1'))==0.5


    j4=MainJoueurIA([Carte('c','4'),Carte('d','3'),Carte('h','3')])
    tapis4=Tapis()
    tapis4.contenu=[Carte('s','J'),Carte('s','3'),Carte('s','5'),Carte('h','J')]
    assert j4.choix_output(tapis4).valeur==4 and j4.choix_output(tapis4).couleur=='c'
    print("+++++choix_output ok+++++\n\n")


    print("*****Tests jeux 1 *****")
    print("+++++tapis 1 : 2 combinaisons possibles car même score+++++")
    #Premier tapis
    j5=MainJoueurIA([Carte('d','5'),Carte('c','7'),Carte('h','6'),Carte('s','J'),Carte('c','1'),Carte('h','Q')])

    tapis_j5_1=Tapis()
    tapis_j5_1.contenu=[Carte('d','3'),Carte('h','5'),Carte('c','4'),Carte('s','7')]
    choisie=j5.choix_output(tapis_j5_1)
    assert choisie==j5.cartes[4]
    print("ok")
    print("+++++tapis 2 : 3 cartes peu de combinaisons de valeur 15 possibles+++++")
    tapis_j5_2=Tapis()
    tapis_j5_2.contenu=[Carte('s','3'),Carte('h','3'),Carte('s','5')]
    choisie=j5.choix_output(tapis_j5_2)
    assert choisie==j5.cartes[1]
    print('ok')
    print("+++++tapis 3 : 2 cartes pas de combinaisons de valeur 15 possibles +++++")
    tapis_j5_3=Tapis()
    tapis_j5_3.contenu=[Carte('h','1'),Carte('s','1')]
    choisie=j5.choix_output(tapis_j5_3)
    assert choisie==j5.cartes[3]
    print("ok")
    print("***** fin tests jeux 1*****\n*****tests jeux 2*****")
    j6=MainJoueurIA([Carte('d','7'),Carte('c','5'),Carte('c','3'),Carte('d','1'),Carte('c','6'),Carte('d','K')])
    print("+++++ tapis 1 : possibilité de scopa+++++")
    tapis_j6_1=Tapis()
    tapis_j6_1.contenu=[Carte('c','2'),Carte('s','2'),Carte('h','2'),Carte('h','J')]
    choisie=j6.choix_output(tapis_j6_1)
    assert choisie==j6.cartes[3]
    print("ok\n+++++tapis 2 : 2 combinaisons de même score mais privilégier 7 de carreau +++++")
    tapis_j6_2=Tapis()
    tapis_j6_2.contenu=[Carte('s','4'),Carte('h','4'),Carte('d','2'),Carte('s','5')]
    choisie=j6.choix_output(tapis_j6_2)
    assert choisie.valeur==7 and choisie.couleur=='d'
    print("OK")
    print("*****fin des tests jeux 2*****\n*****Dernier test mêlant scopa, 7 de carreau*****")
    j7=MainJoueurIA([Carte('s','7'),Carte('c','7'),Carte('h','7'),Carte('d','7'),Carte('s','6'),Carte('d','5')])
    tapis_j7=Tapis()
    tapis_j7.contenu=[Carte('s','4'),Carte('h','4')]
    choisie=j7.choix_output(tapis_j7)
    print(choisie)
    assert choisie.valeur==7 and choisie.couleur=='d'
    print('ok')
    print("**********\nFin des tests pour MainJoueurIA\n**********")
