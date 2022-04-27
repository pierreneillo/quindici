from tkinter import *
from cartes_paquet import Carte, PaquetCartes
from mainjoueur import MainJoueur, MainJoueurIA
from tapis import Tapis
from constantes import *

import time
import copy
from PIL import Image, ImageTk


'''
Cette version de l'interface graphique vient uniquement pour illustrer le jeu
Les interactions avec le joueur se déroulent au clavier dans le shell
Il n'y a pas de clic canvas ni de boutons
'''

class Table:
    '''
    affiche une partie de pharaon

    '''
    def __init__(self, nb_joueurs):
        """
        instancie un objetTable
        """
        nb_cartes = 7
        self.f = Tk()
        self.f.title("Table de jeu")
        self.f.geometry("800x800")
        self.can = Canvas(self.f, width=800, height=800, bg='black')
        self.can.pack(side = LEFT)
        #dessin du tapis de jeu
        self.img_tapis = PhotoImage(file="cards_gif/tapis.png")
        self.can.create_image(0,0,anchor=NW,image=self.img_tapis)
        #création d'une liste de dictionnaires pour chaque position de la table
        self.dicos_images = {position:dict() for position in POSITIONS[nb_joueurs]}
        #on remplit chaque dictionnaire avec les objets Photoimage des cartes
        #orientées selon la position du joueur
        for position in POSITIONS[nb_joueurs]:
            angle = REPERES[position][4]
            for cid in COULEURS:
                for hid in HAUTEURS_SCOPA:
                    id_carte = cid+hid
                    img = Image.open("cards_gif/" + id_carte + ".gif")
                    img_carte=ImageTk.PhotoImage(img.rotate(angle, expand=1))
                    self.dicos_images[position][id_carte]=img_carte
            img_dos = Image.open("cards_gif/dos.gif")
            self.dicos_images[position]["dos"]=ImageTk.PhotoImage(img_dos.rotate(angle, expand=1))






    def clear(self):
        #on efface
        self.can.delete(ALL)
        #on remet juste le tapis vert
        self.can.create_image(0,0,anchor=NW,image=self.img_tapis)


    def espacement_cartes(self, nb_cartes):
        largeur_totale = 2 * DISTANCE
        #print((largeur_totale - CARTE_L * nb_cartes) // nb_cartes)
        return min(0, (largeur_totale - CARTE_L * nb_cartes) // nb_cartes)


    def affiche_cartes(self, position, cartes, hidden = False):
        x_start, y_start, dx, dy, angle = REPERES[position]
        x, y = x_start, y_start
        nb_cartes = len(cartes)
        espace = CARTE_L + self.espacement_cartes(nb_cartes)


        for carte in cartes:
            if hidden == False:
                #ici, on doit créer sur le canvas l'image de la carte
                #l'objet image correspondant se trouve dans le dicos_images
                #A vous :
                image_carte=self.dicos_images[position][carte.id]


            else:
                #ici, le jeu doit être caché, donc on affiche le dos
                #A vous :
                image_carte=self.dicos_images[position]["dos"]
            self.can.create_image(x,y,anchor=NW,image=image_carte)
            x = x + espace * dx
            y = y + espace * dy

    def quitter(self):
        time.sleep(3)
        self.f.destroy()

    def mise_a_jour(self,mains,tapis,vitesse=0):
        """
        Met à jour l'affichage de la table
        """
        assert type(mains)==list,"mains doit être une liste de mains"
        assert type(tapis)==Tapis,"le tapis doit être un objet de classe Tapis"
        time.sleep(vitesse)
        self.can.delete("all")
        self.can.create_image(0,0,anchor=NW,image=self.img_tapis)
        for m in mains:
            assert type(m)==MainJoueur or type(m)==MainJoueurIA,"une main doit être de classe MainJoueur ou MainJoueurIA"
            if m.position != 'S':
                hidd = True
            else:
                hidd = False
            self.affiche_cartes(m.position, m.cartes, hidd)


        #le talon
        #A l'emplacement du talon, on affiche l'image du dos d'une carte
        #à vous
        #.....................................

        #le tapis
        if not tapis.est_vide():
            #A l'emplacement du tapis, on affiche sur le canvas l'image de
            #la première carte se trouvant sur la pile de défausse
            #à vous :
            #...........................................
            x_tapis_start,y_tapis_start,dx,dy,espace=X_TAPIS,Y_TAPIS,1,0,CARTE_L+self.espacement_cartes(len(tapis.contenu))
            x,y=x_tapis_start,y_tapis_start
            for carte in tapis.contenu:
                image_carte=self.dicos_images['N'][carte.id]
                self.can.create_image(x,y,anchor=NW,image=image_carte)
                x = x + espace * dx
                y = y + espace * dy
        self.f.update()

if __name__ == '__main__':
    #à vous d'écrire des tests pour vérifier le fonctionnement de ce module
    table=Table(2)
    j1=MainJoueur([Carte('s','K'),Carte('c','K'),Carte('h','K'),Carte('d','K'),Carte('h','J'),Carte('d','J'),Carte('c','J')],'S')
    j2=MainJoueurIA([Carte('s','Q'),Carte('c','3'),Carte('d','1'),Carte('h','Q'),Carte('c','6'),Carte('s','J'),Carte('d','3')])
    tapis=Tapis()
    tapis.contenu=[Carte('s','2'),Carte('c','4'),Carte('h','J'),Carte('s','3')]
    table.mise_a_jour([j1,j2],tapis)
    table.clear()
    
    table.quitter()


    #terminez par cette ligne pour que la fenêtre Tk ne plante pas
    table.f.mainloop()
