from cartes_paquet import *


class MainJoueur:
    """décris le joueur et son jeu, contient sa position (Nord=ordi sud=joueur)"""

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


    def afficher(self):
        """affiche le jeu trié par valeur de cartes"""
        self.cartes.sort(key=lambda carte:carte.valeur)
        for carte in self.cartes:
            print(carte)


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
        self.plis.append(plis)


    def choix_output(self):
        """récupère le choix du joueur par input texte(= str id_cartes), si le joueur fait une erreur on recommence (pas indéfinimment grâce à l'ajout d'un compteur) """
        present=False
        compteur=0
        while not(present) and compteur!=5:
            compteur+=1
            id_carte=input('saisissez l\'identifaint de la carte')
            id_carte.lower()
            #on vérifie que la carte est présente dans le paquet
            for carte in self.cartes:
                if carte.id==id_carte:
                    present=True
                    choisie=carte
        if compteur==5:
            raise ValueError('Vous passez votre tour : vous auriez dû vous concentrer et saisir le bon id')
        elif present:
            return choisie



#tests
if __name__=='__main__':










##en cours
"""faire les import nécessaires"""

"""demander clic canvas + si bien compris autres méthodes"""

"""faire les tests"""

"""diagramme classes à jour + rajouter attribut id dans classe carte"""
