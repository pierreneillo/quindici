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
                print(carte.id.lower(),id_carte)
                if carte.id.lower()==id_carte:
                    present=True
                    choisie=carte
        if compteur==5:
            print('Vous passez votre tour : vous auriez dû vous concentrer et saisir le bon id')
        elif present:
            return choisie


class MainJoueurIA(MainJoueur):
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
        """prend en paramètre le tapis de jeu pour permettre à l'IA de choisir sa carte à jouer dans le but de marquer plus de points, retourne la carte choisie par l'IA """
        assert type(tapis)==Tapis,"l'objet en paramètre n'est pas un tapis"
        valeur_introuvables=[]#va stocker les valeurs cherchées pour lesquelles il n'y a pas de combinaison possible, afin d'éviter de perdre du temps et de les rechercher après
        resultat=[]#stoke les différentes combiaisons possibles
        contenu_tapis=tapis.contenu
        assert type(contenu_tapis)==list ,"le contenu du tapis n'est pas une liste"
        assert not(tapis.est_vide()),"le tapis est vide"
        #print('ligen 153 tapis avant tri : ',contenu_tapis)
        contenu_tapis=trier(contenu_tapis)#on trie le tapis par valeurs croissantes et les carreaux en avant
        #print('ligne 155 tapis après tri :',contenu_tapis)
        valeurs_introuvables=[]
        #print("ma main est : ",self.cartes)
        for carte in self.cartes:
            assert type(carte)==Carte,"la carte étudiée n'est pas un objet Carte"
            valeur_a_chercher=15-carte.valeur
            if valeur_a_chercher not in valeurs_introuvables:
                combinaisons=self.chercheValeur(valeur_a_chercher,contenu_tapis)#on cherche le 'reste' de la combinaison de 15 points si ce reste n'est pas déjà marqué introuvable
                if combinaisons[0]!=[]:#s'il n'y a pas de combinaisons, combi==[ [] ]
                    #print("combi= ",combinaisons,"vérifier si les cartes sont bien dans le tapis = ",tapis)
                    for combinaison in combinaisons:#on ajoute la carte de la main à toutes les combinaisons trouvées
                        combinaison.append(carte)
                        resultat.append(combinaisons)

                else:
                    valeurs_introuvables.append(valeur_a_chercher)#si on entre ici, il n'y a pas de combinaisons possibles pour la valeur cherchée donc elle est marquée introuvable pour éviter de la rechercher



        #print("resultat= ",resultat)
        #on va chercher la combinaison de score maximum parmi toutes celles recueillies
        maxi=resultat[0][0]#on prend la première combinaison de la première liste de combinaisons
        score_max=self.score_combinaison(maxi)
        for liste_combi in resultat:
            for combi in liste_combi:
                if score_max<self.score_combinaison(combi):
                    maxi=combi
                    score_max=self.score_combinaison(maxi)


        choisie=maxi[-1]#on chosit la dernière carte de meilleure combinaison car il s'agit d'une carte de la main de l'IA



        assert choisie  in self.cartes, "la carte choisie par l'IA n'est pas dans sa main"
        return choisie

    def score_combinaison(self,combinaison):
        """retourne un score flottant entre 0 et 1 à la combinaison passée en paramètre"""
        assert type(combinaison)==list,"la combinaison en paramètre n'est pas une liste"
        score=len(combinaison)#minimum de score possible
        #print("nbr cartes => score= ",score)
        for carte in combinaison:#pour chaque carte de la combinaison,
            assert type(carte)==Carte,"l'objet étudié n'est pas une carte"
            #print("carte étudiée = ",carte)
            if carte.couleur=='d':#on va compter 1 point si carreau car celui qui a le plus de carreaux à la fin marque un point
                score=score+1
                #print("score= ",score)
                #print("valeur carte = ",carte.valeur)
                if carte.valeur==7:#celui qui a le 7 de carreaux marque 1 point à la fin
                    score+=1
                    #print("score= ",score)
            else:
                if carte.valeur==7:#celui qui a le plus de 7 à la fin marque 1 point
                    score=score+1
                    #print("score= ",score)
        #print("score= ",score)
        return score/11#le score maxi est 11 donc pour avoir un ombre entre 0 et 1 on divise par 11






    def chercheValeur(self,valeur_a_chercher,contenu_tapis):
        """prend en paramètre une valeur entière de combinaison de cartes à chercher et le contenu du tapis de jeu trié par valeur croissante de carte, les carreaux étant en avant dans chaque valeur de carte.
        Renvoie une liste de combinaisons(listes) de cartes du tapis"""
        #on vérifie que les variables correspondent à ce qui est attendu
        assert type(valeur_a_chercher)==int,"la valeur à chercher n'est pas un entier"#valeur doit être entier
        assert valeur_a_chercher>=0 and valeur_a_chercher<15,"la valeur cherchée n'appartient pas à [0;15["#compris entre 0 et infèrieure stricte à 15
        assert type(contenu_tapis)==list and contenu_tapis!=[],"le contenu du tapis n'est pas une liste et il n'est pas vide"#on vérifie que le tapis n'est pas vide
        assert len(contenu_tapis)>0 and len(contenu_tapis)<=4,"le tapis contient entre 1 et 4 cartes"
        dico_combinaisons={1:[[0]],
            2:[[0],[1],[0,1]],
            3:[[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]],
            4:[[0],[1],[2],[3],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3],[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1,2,3]]
            }#de la forme clé=taille du contenu de tapis valeur =[tableaux contenant les différentes combinaisons]
        nbr_cartes=len(contenu_tapis)
        #print('nbr cartes tapis',nbr_cartes)
        assert nbr_cartes in dico_combinaisons.keys(),"il y a un problème avec le nombre de cartes"


        combinaisons_possibles=dico_combinaisons[nbr_cartes]
        #print(nbr_cartes," cartes donc : ",combinaisons_possibles)
        resultat=[]
        resultat_modifie=False#booleen qui va nous permettre de savoir si resultat a été modifiée
        for groupe_indices in combinaisons_possibles:
            #print("groupe indices évalués",groupe_indices)
            somme=0
            combi_en_cours=[]
            #print("somme = ",somme)
            for indice in groupe_indices:
                carte=contenu_tapis[indice]#contenu_tapis[indice] est une carte
                assert type(carte)==Carte,"l'objet étudié n'est pas un objt carte"
                #print(carte)
                somme+=carte.valeur
                #print("somme = ",somme)
                combi_en_cours.append(carte)
                #print("combi_en_cours = ",combi_en_cours)
            if somme==valeur_a_chercher:
                resultat.append(combi_en_cours)
                resultat_modifie=True
                #print('resultat= ',resultat)
        if not(resultat_modifie):
            return [[]]#resultat étant une liste de combinaisons, pour garder cette structure on renvoie une lise composée d'une liste vide
        else:
            return resultat

def trier(contenu_tapis):
    """trie le contenu du tapis passé en pramètre par valeur et en ayant les carreaux en avant dans chaque valeur, on utilise pour cela l'attribut valeur2 de la classe Carte qui enlève 0.1 à chaque valeur d'une carte de couleur carreau"""
    assert contenu_tapis!=[],"le tapis est vide"
    resultat=sorted(contenu_tapis,key=lambda x:x.valeur2)
    return resultat









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

    print('\n ----- Deuxième version : méthodes : choix_output(tapis), score_combinaison(combinaison), chercheValeur(valeur_a_chercher,contenu_tapis); \n fonctions : -trier(contenu_tapis)-----')
    tapis=Tapis()
    tapis.contenu=[Carte('c','7'),Carte('d','7'),Carte('h','5'),Carte('d','5')]
    print("tapis avant tri : ",tapis.contenu)
    contenu1=tapis.contenu
    contenu1=trier(contenu1)#trier ok
    print("tapis après tri : ",contenu1)
    print('+++++trier ok+++++')
    #print([Carte('d','5'),Carte('h','5'),Carte('d','7'),Carte('c','7')])

    combi2=j3.chercheValeur(14,contenu1)#resultat attendu 1 combinaison
    assert len(combi2)==1
    combi1=j3.chercheValeur(12,contenu1)#resultat attendu 4 combinaisons
    assert len(combi1)==4
    combi3=j3.chercheValeur(11,contenu1)#resultat attendu 1 combinaison vide
    assert len(combi3)==1 and combi3[0]==[]
    print("+++++chercheValeur OK+++++")

    assert j3.score_combinaison(combi3[0])==0/11#combinaison vide
    #print(j3.score_combinaison(combi1[0])*11)
    assert j3.score_combinaison(combi1[0])==(2+1+1+1)/11
    assert j3.score_combinaison(combi2[0])==(2+1+1+1)/11
    print("+++++score_combinaison ok+++++")

    choisie=j3.choix_output(tapis)
    assert choisie.valeur==1 and choisie.hauteur=='1' and choisie.couleur=='d'
    j4=MainJoueurIA([Carte('c','4'),Carte('d','3'),Carte('h','3')])
    tapis4=Tapis()
    tapis4.contenu=[Carte('s','J'),Carte('s','3'),Carte('s','5'),Carte('h','J')]
    assert j4.choix_output(tapis4).valeur==4 and j4.choix_output(tapis4).couleur=='c'
    print("+++++choix_output ok+++++")





