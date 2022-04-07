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
            if carte.id==id_carte:
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



    def score(self,carte):
        '''quantifie l'intérêt de jouer la carte en paramètre,renvoie un nombre entre 0 et 1 '''
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


    def choix_output(self):
        """récupère le choix du joueur par input texte(= str id_cartes), si le joueur fait une erreur on recommence (pas indéfinimment grâce à l'ajout d'un compteur) """
        return random.choice(self.cartes)





#tests
if __name__=='__main__':


    #tests MainJoueur
    print('début des tests pour MainJoueur')
    #tests constructeur
    j1=MainJoueur([Carte('c','Q'),Carte('d','5'),Carte('h','1')],'S')
    j2=MainJoueur([],'N')

    assert not(j1.est_vide())#est_vide() ok
    assert j2.est_vide()
    j1.afficher()#afficher ok
    j2.afficher()
    j1.recevoir(Carte('d','4'))#recevoir ok
    j2.recevoir(Carte('d','2'))
    j1.afficher()
    j2.afficher()
    j1.rejeter('h1')#rejeter ok
    j2.rejeter('d2')
    j1.afficher()
    j2.afficher()
    print(j1.plis)
    print(j2.plis)
    j1.ajoute_plis(PaquetCartes(40).cartes)#ajoute_plis ok
    j2.ajoute_plis(PaquetCartes(40).cartes)
    print(j1.plis)
    print(j2.plis)
    print('test choix output',j1.choix_output())
    j1.afficher()


    print('Début des tests pour MainJoueurIA')
    j3=MainJoueurIA([Carte('h','Q'),Carte('c','7'),Carte('d','1')],'N')
    print(j3.choix_output())
    j3.score(Carte('h','Q'))





