import random
from cartes_paquet import Carte, PaquetCartes
from mainjoueur import MainJoueur,MainJoueurIA
from tapis import Tapis
from constantes import *
from table import Table






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
    @table: l'objet de classe table dont on a besoin pour la représentation graphique
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
        self.nb_cartes = nb_cartes
        self.nb_par_joueur = nb_par_joueur

        #création des mains des joueurs
        # vides au départ !
        #à vous
        self.mains = [MainJoueur([],POSITIONS[self.nb_joueurs][i]) for i in range(self.nb_joueurs)]
        if self.nb_joueurs==2:
            self.mains = [self.mains[0],MainJoueurIA([],POSITIONS[2][1])]
        #création de la table
        self.table=Table(self.nb_joueurs)


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
        '''
        Renvoie une chaîne représentant le tapis et les mains
        '''
        s = ""
        s += repr(self.tapis) + "\n"
        s += "Mains : \n"
        for main in self.mains:
            s += repr(main) + "\n"
        return s

    def distribuer(self):
        '''
        Remplit les listes de cartes des mains pour chaque joueur
        '''
        servi = (self.donneur + 1) % self.nb_joueurs
        #servi est l'indice du joueur à qui donner une carte
        for _ in range(self.nb_par_joueur):
            for _ in range(self.nb_joueurs):
                #on distribue une carte à ce joueur
                self.mains[servi].recevoir(self.paquet.tirer())
                #au prochain tour, ce sera au joueur suivant
                servi = (servi + 1) % self.nb_joueurs





    def start(self,cas_de_base=4):
        '''
        mélange le paquet, coupe, distribue les cartes
        pose cas_de_base cartes sur le tapis
        n'affiche plus le tout car sinon le joueur voit le jeu de l'IA
        puis affiche ("on démarre")
        '''
        self.paquet.battre()
        self.paquet.couper()
        self.distribuer()
        for _ in range(cas_de_base):
            self.tapis.ajouter(self.paquet.tirer())
        print("jeu IA :")
        #self.mains[1].afficher()# NE PAS DECOMMENTER, sinon le joueur verra le jeu de l'IA
        print("on démarre")

    def simul_jeu(self):
        '''
        Simule une partie (1 tour):
            -Lance la partie
            -Fait jouer le Joueur et l'IA tant que les deux jeux ne sont pas vides
        '''
        for i in range(3):
            if i==0:self.start()
            elif i>0:self.start(0)
            #Pour l'instant le joueur commence dans tous les cas
            while sum([int(not main.est_vide()) for main in self.mains])!=0:#Si au moins une main contient encore des cartes
                #1 tour de boucle = 1 tour de jeu
                #A 2 joueurs, le 'vrai' joueur est au Sud, soit à la position 0
                #---------------------------Le 'vrai' joueur joue------------------------------------
                self.table.mise_a_jour(self.mains,self.tapis)
                print("Votre jeu :")#,self.mains[0])
                self.mains[0].afficher()
                print(self.tapis)
                id_carte_a_jouer = self.mains[0].choix_output().id
                carte_jouee = self.mains[0].rejeter(id_carte_a_jouer)
                self.tapis.ajouter(carte_jouee)
                self.table.mise_a_jour(self.mains,self.tapis)
                print(f"Vous avez joué {carte_jouee}")
                quindici,combi_opt = self.tapis.tester_quindici()
                if quindici:
                    if self.tapis.scopa:
                        print("Scopa! Vous ramassez toutes les cartes")
                        self.mains[0].nb_scopa+=1
                    else:
                        print("Quindici! Vous ramassez les cartes :", "-".join([str(c) for c in combi_opt]))
                    #print(list(combi_opt))
                    combi_opt=list(combi_opt)
                    self.mains[0].ajoute_plis(combi_opt)
                    for carte in combi_opt:
                        self.tapis.enlever(carte.id)
                else:
                    print("Dommage :( vous n'avez rien ramassé cette fois-ci...")

                print(self.tapis)
                self.table.mise_a_jour(self.mains,self.tapis,2)
                #---------------------------------L'IA joue----------------------------------------
                id_carte_a_jouerIA = self.mains[1].choix_output(self.tapis).id
                carte_joueeIA = self.mains[1].rejeter(id_carte_a_jouerIA)
                self.tapis.ajouter(carte_joueeIA)
                self.table.mise_a_jour(self.mains,self.tapis)
                print(f"L'IA a joué {carte_joueeIA}")
                quindici,combi_opt = self.tapis.tester_quindici()
                combi_opt=list(combi_opt)
                if quindici:
                    if self.tapis.scopa:
                        self.mains[1].nb_scopa+=1
                        print("Scopa! L'IA ramasse toutes les cartes")
                    else:
                        print("Quindici! L'IA ramasse les cartes :", "-".join([str(c) for c in combi_opt]))
                    self.mains[1].ajoute_plis(combi_opt)
                    for carte in combi_opt:
                        self.tapis.enlever(carte.id)
                else:
                    print("L'IA n'a rien ramassé cette fois-ci...")
                print(self.tapis)
                self.table.mise_a_jour(self.mains,self.tapis,2)
            self.table.mise_a_jour(self.mains,self.tapis,2)
            print(f"+++++++++++FIN DU TOUR {i}++++++++++")
        #------compter les points de fin de partie
        self.compte_points_fin()
        #afficher les scores
        self.affiche_vainqueur()
        self.table.quitter()


    def compte_points_fin(self):
        """ comptabilise les points à la fin de la parie"""
        #on stocke toutes les informations
        nbr_cartes_0=len(self.mains[0].plis)
        print("nbr_cartes_0= ",nbr_cartes_0)
        nbr_cartes_1=len(self.mains[1].plis)
        print("nbr_cartes_1= ",nbr_cartes_1)
        nbr_ecus_0=self.mains[0].compte_ecus()
        nbr_ecus_1=self.mains[1].compte_ecus()
        print("nbr_ecus_0= ",nbr_ecus_0,"\n nbr_ecus_1= ",nbr_ecus_1)
        nbr_7_0=self.mains[0].compte_7()
        nbr_7_1=self.mains[1].compte_7()
        print("nbr_7_0= ",nbr_7_0,"\n nbr_7_1= ",nbr_7_1)
        ecu_7_0=self.mains[0].ecu_7()
        ecu_7_1=not(ecu_7_0)
        print("ecu_7_0= ",ecu_7_0,"\n ecu_7_1= ",ecu_7_1)
        # et on les compare : nbr_cartes
        if nbr_cartes_0<nbr_cartes_1:
            self.mains[1].nb_scopa+=1
        elif nbr_cartes_0==nbr_cartes_1:
            self.mains[1].nb_scopa+=1
            self.mains[0].nb_scopa+=1
        else:
            self.mains[0].nb_scopa+=1
        # nbr_ecus:
        if nbr_ecus_0<nbr_ecus_1:
            self.mains[1].nb_scopa+=1
        elif nbr_ecus_0==nbr_ecus_1:
            self.mains[1].nb_scopa+=1
            self.mains[0].nb_scopa+=1
        else:
            self.mains[0].nb_scopa+=1
        # nbr_7 :
        if nbr_7_0<nbr_7_1:
            self.mains[1].nb_scopa+=1
        elif nbr_7_0==nbr_7_1:
            self.mains[1].nb_scopa+=1
            self.mains[0].nb_scopa+=1
        else:
            self.mains[0].nb_scopa+=1
        # ecu_7 :
        if ecu_7_1:
            self.mains[1].nb_scopa+=1
        elif ecu_7_0:
            self.mains[0].nb_scopa+=1

    def affiche_vainqueur(self,graph=0):
        """affiche la position du vainqueur, si le paramètre graph est renseigné : affichage graphique sinon dans le shell"""
        #on désigne le vainqueur
        vainqueur=self.mains[1].position
        score=self.mains[1].nb_scopa
        if self.mains[0].nb_scopa>score:
            vainqueur=self.mains[0].position
            score=self.mains[0].nb_scopa
        elif score==self.mains[0].nb_scopa:
            vainqueur=None
            score=0
        #on passe à l'affichage
        if graph==0:
            if vainqueur!=None: print(f"le joueur en position {vainqueur} a gagné avec un score de {score}")
            else: print("Egalité personne ne remporte ce duel")
        else:
            pass#à compléter si on a le temps










#test
if __name__ == '__main__':

    test = Partie()
    #tests pour la fonction simul_jeu()
    test.simul_jeu()

