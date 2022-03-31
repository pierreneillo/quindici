import random
from cartes_paquet import Carte, PaquetCartes
from mainjoueur import MainJoueur
from tapis import Tapis
from constantes import *






## la classe principale (la plus haute) : prépare et lance la partie
class Partie:
    '''
    Modélise une partie de Quindici
    1 joueur contre 1 IA
    Attributs
    @nb_joueurs : int valant 2 par défaut
    @nb_cartes : int valant 40 par défaut
    @nb_par_joueur : int valant 6 par défaut
    @paquet : un objet de la classe Paquet
    @tapis : un objet de la classe Tapis
    @mains : liste d'objets de type MainJoueur, représentant les joueurs
    de la Partie (et leur jeu)
    @donneur : int représentant l'indice du joueur qui va distribuer
    dans la liste des mains

    Méthodes
    @afficher() : fait afficher les mains des joueurs et le tapis
    @distribuer() : remplit les mains des joueurs avec les cartes du paquet
    @start() : prépare tout pour le début du jeu
    @simul_jeu() : simule une partie courte de jeu (1 tour)
    ...

    '''
    def __init__(self, nb_joueurs=2, nb_cartes=40, nb_par_joueur=6):

        #vérification de routine
        if nb_joueurs < 1 or nb_joueurs > 4 or \
        (nb_cartes != 32 and nb_cartes != 52 and nb_cartes != 40) or \
         nb_par_joueur > nb_cartes // nb_joueurs:
            raise ValueError(VALUE_ERROR)



        #génération du paquet de carte pour le jeu
        self.paquet = PaquetCartes(nb_cartes)
        self.tapis = Tapis()

        self.nb_joueurs = nb_joueurs
        self.donneur = 0

        self.nb_par_joueur = nb_par_joueur

        #création des mains des joueurs
        # vides au départ !
        #à vous
        self.mains = [MainJoueur([],POSITIONS[self.nb_joueurs][i]) for i in range(self.nb_joueurs)]


    def afficher(self):
        '''
        affiche les jeux des joueurs
        et le tapis
        '''
        print("Tapis :",self.tapis)
        print("Mains :")
        for main in self.mains:
            print(main)

    def __repr__(self):
        s = ""
        s += repr(self.tapis) + "\n"
        s += "Mains : \n"
        for main in self.mains:
            s += repr(main) + "\n"
        return s

    def distribuer(self):
        '''
        remplit les listes de cartes des mains pour chaque joueur
        '''
        servi = (self.donneur + 1) % self.nb_joueurs
        #servi est l'indice du joueur à qui donner une carte
        for _ in range(self.nb_par_joueur):
            for _ in range(self.nb_joueurs):
                #on distribue une carte à ce joueur
                self.mains[servi].recevoir(self.paquet.tirer())
                #au prochain tour, ce sera au joueur suivant
                servi = (servi + 1) % self.nb_joueurs





    def start(self):
        '''
        mélange le paquet, coupe, distribue les cartes
        pose 4 cartes sur le tapis
        n'affiche plus le tout car sinon le joueur voit le jeu de l'IA
        puis affiche ("on démarre")
        '''
        self.paquet.battre()
        self.paquet.couper()
        self.distribuer()
        for _ in range(4):
            self.tapis.ajouter(self.paquet.tirer())
        #print(self) NE PAS DECOMMENTER, sinon le joueur verra le jeu de l'IA
        print("on démarre")

    def simul_jeu(self):
        '''
        Simule une partie (1 tour):
            -Lance la partie
            -Fait jouer le Joueur et l'IA tant que les deux jeux ne sont pas vides
        '''
        self.start()
        #Pour l'instant le joueur commence dans tous les cas
        while sum([int(main.est_vide()) for main in self.mains])!=0:#Si au moins une main contient encore des cartes
            #1 tour de boucle = 1 tour de jeu
            #A 2 joueurs, le 'vrai' joueur est au Sud, soit à la position 0
            #---------------------------Le 'vrai' joueur joue------------------------------------
            print("Votre jeu :",self.mains[0])
            print(self.tapis)
            id_carte_a_jouer = self.mains[0].choix_output()
            carte_jouee = self.mains[0].rejeter(id_carte_a_jouer)
            self.tapis.ajouter(carte_jouee)
            print(f"Vous avez joué {carte_jouee}")
            quindici,combi_opt = self.tapis.tester_quindici()
            if quindici:
                if self.tapis.scopa:
                    print("Scopa! Vous ramassez toutes les cartes")
                else:
                    print("Quindici! Vous ramassez les cartes :", "-".join(combi_opt))
                self.mains[0].ajoute_plis(combi_opt)
                for carte in combi_opt:
                    self.tapis.enlever(carte.id)
            else:
                print("Dommage :( vous n'avez rien ramassé cette fois-ci...")
            
            print(self.tapis)
            #---------------------------------L'IA joue----------------------------------------
            id_carte_a_jouerIA = self.mains[0].choix_output()
            carte_joueeIA = self.mains[0].rejeter(id_carte_a_jouerIA)
            self.tapis.ajouter(carte_joueeIA)
            print(f"L'IA a joué {carte_joueeIA}")
            quindici,combi_opt = self.tapis.tester_quindici()
            if quindici:
                if self.tapis.scopa:
                    print("Scopa! L'IA ramasse toutes les cartes")
                else:
                    print("Quindici! L'IA ramasse les cartes :", "-".join(combi_opt))
                self.mains[0].ajoute_plis(combi_opt)
                for carte in combi_opt:
                    self.tapis.enlever(carte.id)
            else:
                print("L'IA rien ramassé cette fois-ci...")
            print(self.tapis)
            
            
            
        



#test
if __name__ == '__main__':
    test = Partie()
    test.start()
