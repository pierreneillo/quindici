
# ---
# --- CONSTANTES POUR LE MODELE

COULEURS = ['c', 'd', 'h', 's']
HAUTEURS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
HAUTEURS_SCOPA = ['1', '2', '3', '4', '5', '6', '7', 'J', 'Q', 'K']
#couleurs : c, d, h, s correspondant à 0, 1, 2, 3
#clubs, diamonds , hearts and spades.
#hauteurs : 1 pour l'As jusqu'à 10 pour le 10, puis J, Q, K
#J pour Jack (Valet), Q pour Queen et K pour King
#correspondant aux indices de 0 à 12 (As au Roi)


DICO_COULEURS = {'c':0, 'd':1, 'h':2, 's':3}
DICO_HAUTEURS = {'1':0, '2':1, '3':2, '4':3, '5':4,
    '6':5, '7':6, '8':7, '9':8, '10':9, 'J':10, 'Q':11, 'K':12}
DICO_VALEURS = {'1':1, '2':2, '3':3, '4':4, '5':5,
    '6':6, '7':7, '8':None, '9':None, '10':None, 'J':8, 'Q':9, 'K':10}
#au pharaon, chaque carte représente un nombre de points égale à sa valeur faciale (1 pour l'As, 2 pour 2...)
#sauf les honneurs qui valent chacun 10 points
#DICO_VALEURS = ....

# Positions des joueurs en fonction du nombre
# 2 joueurs : Sud et Nord
# 3 joueurs : Sud, Est et Nord
# 4 joueurs : Sud, Est, Nord et Ouest

POSITIONS = '', 'S', 'SN', 'SEN', 'SENO'



VALUE_ERROR = 'nb_joueurs doit être entre 2 et 4, nb_cartes est égal à 32 ou à 52, ou à 40'


# ---
# --- CONSTANTES POUR LA VUE TKINTER

# distance au centre du tapis en pixel
DISTANCE = 400



#dimensions des images des cartes
CARTE_H = 96
CARTE_L = 71

#TAPIS et TALON
X_TAPIS, Y_TAPIS = 425, 350
X_TALON, Y_TALON = 350,350


# permettra de positionner correctement
# les cartes en fonction de la position
# du joueur à table
# les cartes sont posées face au joueur
# de sa gauche vers sa droite
# pour chaque position on a le x_start, y_start, dx, dy et orientation
#
#                 N
#      dx: -1, dy: 0, orientation: 180
#                    ←
#               🂪🂫🂭🂮🂡
#
#270↓🂪                            🂪
#    🂫                            🂪
# O  🂪        centre de           🂪  E
#    🂪        la table            🂪
#    🂪                            🂪 ↑ 90
# dx:0                           dx: 0
# dy: 1                           dy: -1
#               🂪🂫🂭🂮🂡
#               →
#                  S
#      dx: 1, dy: 0, orientation: 0

REPERES = { 'S':(70,600, 1, 0, 0), 'E':(700,620,0, -1, 90),
        'N':(670, 0, -1, 0, 180), 'O':(0, 20,0, 1, 270)}