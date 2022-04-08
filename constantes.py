__about__ = """Module constantes.py: constantes pour le jeu de scopa
----------------------------------------------------------------------------
| Variable            | Utilisation/Signification                          |
|__________________________________________________________________________|
|                     |                                                    |
| COULEURS            | Les quatres couleurs du jeu de cartes:             |
|                     | clubs, diamonds, hearts et spades                  |
----------------------------------------------------------------------------
| HAUTEURS_SCOPA      | Les valeurs de cartes du jeu de scopa              |
----------------------------------------------------------------------------
| DICO_COULEURS       | Associe chaque couleur à son indice dans COULEURS  |
----------------------------------------------------------------------------
| DICO_HAUTEURS_SCOPA | Associe chaque hauteur à son indice dans HAUTEURS  |
----------------------------------------------------------------------------
| DICO_VALEURS        | Associe chaque hauteur à sa valeur dans le jeu     |
----------------------------------------------------------------------------
|                     | Positions des joueurs en fonction du nombre        |
| POSITIONS           |   - 2 joueurs : Sud et Nord                        |
|                     |   - 3 joueurs : Sud, Est et Nord                   |
|                     |   - 4 joueurs : Sud, Est, Nord et Ouest            |
----------------------------------------------------------------------------
| VALUE_ERROR         | L'erreur devant être renvoyée lorsqu'il y a une    |
|                     | incohérence dans la construction du paquet         |
----------------------------------------------------------------------------
|                          Attributs graphiques                            |
----------------------------------------------------------------------------
| DISTANCE            | Distance au centre du tapis en pixels              |
----------------------------------------------------------------------------
| CARTE_H, CARTE_L    | Dimensions des images des cartes                   |
----------------------------------------------------------------------------
| X_TAPIS, Y_TAPIS    | Coordonnées du tapis                               |
----------------------------------------------------------------------------
| X_TALON, Y_TALON    | Coordonnées du talon                               |
----------------------------------------------------------------------------
| REPERES             | Repères pour la position des mains des joueurs     |
----------------------------------------------------------------------------
"""

COULEURS = ['c', 'd', 'h', 's']
HAUTEURS_SCOPA = ['1', '2', '3', '4', '5', '6', '7', 'J', 'Q', 'K']


DICO_COULEURS = {'c':0, 'd':1, 'h':2, 's':3}
DICO_HAUTEURS_SCOPA = {'1':0, '2':1, '3':2, '4':3, '5':4,
    '6':5, '7':6, 'J':7, 'Q':8, 'K':9}
DICO_VALEURS = {'1':1, '2':2, '3':3, '4':4, '5':5,
    '6':6, '7':7, '8':None, '9':None, '10':None, 'J':8, 'Q':9, 'K':10}

POSITIONS = '', 'S', 'SN', 'SEN', 'SENO'



VALUE_ERROR = 'nb_joueurs doit être entre 2 et 4, nb_cartes est égal à 32 ou à 52, ou à 40'

DISTANCE = 400

CARTE_H = 96
CARTE_L = 71

X_TAPIS, Y_TAPIS = 425,350
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
