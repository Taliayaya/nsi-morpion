# Multi-Threading à installer

import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN
from pygame.cursors import diamond # Forme de curseur

#Déclaration de constantes, C is better tho
COULEUR_FOND = (180,50,0)
COULEUR_DESSIN = (0,0,255)
COULEUR_CLIGNO = (0,255,0)
LARGEUR_LIGNE = 8
DIMENSIONS_GRILLE = 320
PLACE_GRILLE_VERTI = 220
PLACE_GRILLE_HORI = 120

class Case(pg.Rect):
    def __init__(self, left, top, width, height, posx = -1, posy = -1):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.lit = False
        self.pos = (posx, posy)
    def light(self):
        self.lit = not(self.lit)
        if self.lit :
            pg.draw.rect(surf,COULEUR_CLIGNO,((self.left+1,self.top+1),(self.width,self.height)),LARGEUR_LIGNE-5)
        else :
            self.eteindre()
    def eteindre(self):
        self.lit = False
        pg.draw.rect(surf,COULEUR_DESSIN,((self.left+1,self.top+1),(self.width,self.height)),LARGEUR_LIGNE-5)
    def dessiner(self, value): #-1 Pour rien, 0 pour Croix, 1 pour Rond
        pg.draw.rect(surf,COULEUR_FOND,((self.left + 5,self.top + 5),\
                                        (self.width - LARGEUR_LIGNE,self.height - LARGEUR_LIGNE)),0)
        if not(value):
            pg.draw.line(surf,COULEUR_DESSIN,(self.topleft[0]+10,self.topleft[1]+10),\
                         (self.bottomright[0]-10, self.bottomright[1]-10), LARGEUR_LIGNE)
            pg.draw.line(surf,COULEUR_DESSIN,(self.topright[0]-10,self.topright[1]+10),\
                         (self.bottomleft[0]+10, self.bottomleft[1]-10), LARGEUR_LIGNE)
        elif value == 1 : #A éventuellement transformer en if else booléen si la fonction d'effacement n'est pas utilisée
            pg.draw.circle(surf,COULEUR_DESSIN,(self.width/2 + self.topleft[0] + 1,\
                                                self.height/2+ self.topleft[1] + 1),\
                           (self.height/2-6), 5)

class Grid():
    def __init__(self, dimx, dimy, wincond): # A voir si les cases de contrôle et les tours seront gérés ici
        casex = DIMENSIONS_GRILLE/dimx #Valeurs qui seront peut être changeables à l'avenir
        casey = DIMENSIONS_GRILLE/dimy
        #Cases de contrôle
        self.case_croix = Case(280,500,80,80) #Positions des cases de contrôle
        self.case_rond = Case(410,500,80,80)
        pg.draw.rect(surf,COULEUR_CLIGNO,(280,500,80,80),5)
        pg.draw.rect(surf,COULEUR_CLIGNO,(410,500,80,80),5)
        # Valeurs
        self.wincond = wincond
        self.layout = []
        self.hauteur = dimx
        self.largeur = dimy
        ligne = [-1] * dimy
        self.positions = []
        for i in range(dimx):
            self.positions.append(ligne.copy())
        # Création dans une liste des cases contenues et dessin du plateau de jeu
        start_vertical = PLACE_GRILLE_VERTI
        start_horizontal = PLACE_GRILLE_HORI
        for x in range(dimx):
            pg.draw.line(surf, COULEUR_DESSIN,(start_vertical, 100),(start_vertical, 460),LARGEUR_LIGNE)
            self.layout.append([Case(y*casey+PLACE_GRILLE_VERTI, x*casex+PLACE_GRILLE_HORI, casey, casex, x, y)\
                                for y in range(dimy)])
            pg.draw.line(surf, COULEUR_DESSIN,(200, start_horizontal),(560, start_horizontal), LARGEUR_LIGNE)
            start_horizontal = start_horizontal + casey
            pg.draw.line(surf, COULEUR_DESSIN,(200, start_horizontal),(560, start_horizontal), LARGEUR_LIGNE)
            start_vertical = start_vertical + casex
        pg.draw.line(surf, COULEUR_DESSIN,(start_vertical, 100),(start_vertical, 460),LARGEUR_LIGNE)

    def showturn(self, player):
        if player :
            self.case_croix.dessiner(-1)
            self.case_rond.dessiner(1)
        else:
            self.case_rond.dessiner(-1)
            self.case_croix.dessiner(0)

    def __getitem__(self, key):
        return self.layout[key[0]][key[1]]

    def __del__(self):
        surf.fill(COULEUR_FOND)

    def check(self, posx, posy, value):
        #Cherche si le joueur value a gagné avec le coup joué en (posx, posy)
        #Renvoie 0 si rien n'est trouvé, et 1 si le joueur est gagnant

        for i in range(max(0,posy+1-self.wincond), min(self.largeur-self.wincond, posy)+1):
        #Check les lignes
            for j in range(self.wincond):
                if not(self.positions[posx][i+j] == value):
                    break
                elif j == self.wincond-1 :
                    return 1

        for i in range(max(0,posx+1-self.wincond), min(self.hauteur-self.wincond, posx)+1):
        #Check les colonnes
            for j in range(self.wincond):
                if not(self.positions[i+j][posy] == value):
                    break
                elif j == self.wincond-1 :
                    return 1

        #Check la diagonale du haut-gauche au bas-droite
        #Coordonnées du point auquel la diagonale commence
        point_debut = (max(posx-min(self.wincond, posy), 0), max(posy-min(self.wincond, posx), 0))
        i=0
        while(i+self.wincond<min(self.hauteur-point_debut[0],self.largeur-point_debut[1])+1):
            for j in range(self.wincond):
                if not(self.positions[point_debut[0]+i+j][point_debut[1]+i+j] == value):
                    break
                elif j== self.wincond-1:
                    return 1
            i+=1

        #Check la diagonale du haut-droite au bas-gauche
        #Coordonnées du point auquel la diagonale commence
        point_debut = (max(posx-min(self.wincond-1, self.largeur-posy-1), 0),\
                           min(posy + min(posx, self.wincond-1), self.largeur-1))
        i=0
        while(i+self.wincond<min(self.hauteur-point_debut[0],point_debut[1]+1)+1):
            for j in range(self.wincond):
                if not(self.positions[point_debut[0]+i+j][point_debut[1]-i-j] == value):
                    break
                elif j==self.wincond-1:
                    return kuraO
            i+=1

        #Rien trouvé
        return 0

def init():
    """Portion à faire dans le design POSIX"""
    global surf #Le surf est global pour que toutes les fonctions puissent l'utiliser
    surf = pg.display.set_mode((800,600),0,10)
    pg.display.set_caption("Morpion","Morpion")
    pg.display.set_allow_screensaver(True)
    pg.mouse.set_cursor(diamond)
    surf.fill(COULEUR_FOND)
    # Fenêtre de choix de la configuration, dans une boucle infinie
    run(6, 6, 3)
    # Fenêtre pour rejouer (et boucle à installer)
    pg.quit()


def run(hauteur, largeur, wincondition):
    running = True
    grille = Grid(hauteur, largeur, wincondition)
    timer = 0
    xactuel = 0 #Les coordonnées à mettre à jour
    yactuel = 0
    player_actuel = 0 #Echange entre 0 (croix) et 1 (rond)
    grille.showturn(player_actuel)
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if xactuel:
                        grille[(xactuel,yactuel)].eteindre()
                        xactuel -=1
                elif event.key == pg.K_DOWN:
                    if xactuel != hauteur-1 :
                        grille[(xactuel,yactuel)].eteindre()
                        xactuel += 1
                elif event.key == pg.K_RIGHT:
                    if yactuel != largeur-1 :
                        grille[(xactuel,yactuel)].eteindre()
                        yactuel += 1
                elif event.key == pg.K_LEFT:
                    if yactuel:
                        grille[(xactuel,yactuel)].eteindre()
                        yactuel -= 1
                elif event.key == pg.K_SPACE: # Permet de placer sa pièce
                    if grille.positions[xactuel][yactuel] == -1: #Vérifie que la case est vide
                        grille[(xactuel,yactuel)].dessiner(player_actuel)
                        grille.positions[xactuel][yactuel] = player_actuel
                        if (grille.check(xactuel, yactuel, player_actuel)):
                                running = False
                                print(f"Victoire du joueur {player_actuel +1} !")
                                # Passage à la prochaine partie
                        player_actuel = abs(1-player_actuel) # Change de joueur
                        grille.showturn(player_actuel)
                elif event.key == pg.K_RETURN: #Permet de réinitialiser la partie
                    running = False
                    del(grille)
                    #Passage à la prochaine partie
        # if event.type == MOUSEBUTTONDOWN(1,0,0):  event qui va premettre par la suite de connaitre la
        # position de la souris lorsqu'on clique dessus pour pouvoir quelle case select ou lightup
        pg.display.flip()
        timer += 1
        if timer == 255:
            timer = 0
            grille[(xactuel,yactuel)].light()
        if event.type == pg.QUIT:
            running = False
            pg.quit()

def main():
    init()

if __name__ == "__main__":
    main()
