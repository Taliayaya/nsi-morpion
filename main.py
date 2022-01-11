#!/usr/bin/env python3
import pygame
import AI_easy
import AI_difficult

# Window Size
WINDOWSIZE = 600  # aussi disponible en 900

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (139, 0, 0)

# Case selection images
X = pygame.image.load('assets/images/X.png')
O = pygame.image.load('assets/images/O.png')
VICTORY_X = pygame.image.load('assets/images/victoryX.png')
VICTORY_O = pygame.image.load('assets/images/victoryO.png')


class Morpion:
    def __init__(self, windowSize: int) -> None:
        self.windowSize = windowSize
        self.turn = 0
        self.morpion = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.canPlay = True
        self.maxTurn = 9
        self.difficult = False
        self.isPlayingVsAI = True
        self.showTuto = True
        ####
        # Permet de calculer les dimensions des cases
        # à partir de la taille de la fenêtre indiquée (WINDOWSIZE)
        ####
        if (windowSize-12) % 3 == 0:
            border = 3
            length = (windowSize-12)//3  # coté d'une case
            self.coordColumn1 = border
            self.coordColumn2 = self.coordColumn1+border+length
            self.coordColumn3 = self.coordColumn2+border+length

            # Définie les emplacements de chaque case
            self.coordonneesCasesX1 = [
                self.coordColumn1, self.coordColumn2, self.coordColumn3]*3
            self.coordonneesCasesY1 = [self.coordColumn1, self.coordColumn1, self.coordColumn1, self.coordColumn2,
                                       self.coordColumn2, self.coordColumn2, self.coordColumn3, self.coordColumn3, self.coordColumn3]
            self.coordonneesCasesX2 = [length]*9
            self.coordonneesCasesY2 = [length]*9

            # Redimensionne les images pour rentrer dans les cases
            self.X = pygame.transform.scale(X, (length, length))
            self.O = pygame.transform.scale(O, (length, length))
            self.victory_O = pygame.transform.scale(
                VICTORY_O, (length, length))
            self.victory_X = pygame.transform.scale(
                VICTORY_X, (length, length))

        self.surf = pygame.display.set_mode((self.windowSize, self.windowSize))
        pygame.display.set_caption('Jeu de morpion')

    def handleVictory(self):
        """Gère tous les cas de victoire possible
        Renvoie un tuple contenant la lettre du gagnant
        ainsi que l'indice des cases qui ont permis la victoire
        """
        if self.morpion[0][0] == self.morpion[0][1] == self.morpion[0][2] and not self.morpion[0][0] == 0:
            # correspond à :
            # X X X
            # 0 0 0
            # 0 0 0
            print('VICTORY')
            return self.morpion[0][0], (0, 1, 2)
        elif self.morpion[1][0] == self.morpion[1][1] == self.morpion[1][2] and not self.morpion[1][0] == 0:
            # correspond à :
            # 0 0 0
            # X X X
            # 0 0 0
            print('VICTORY')
            return self.morpion[1][0], (3, 4, 5)
        elif self.morpion[2][0] == self.morpion[2][1] == self.morpion[2][2] and not self.morpion[2][0] == 0:
            # correspond à :
            # 0 0 0
            # 0 0 0
            # X X X
            print('VICTORY')
            return self.morpion[2][0], (6, 7, 8)
        elif self.morpion[0][0] == self.morpion[1][0] == self.morpion[2][0] and not self.morpion[0][0] == 0:
            # correspond à :
            # X 0 0
            # X 0 0
            # X 0 0
            print('VICTORY')
            return self.morpion[0][0], (0, 3, 6)
        elif self.morpion[0][1] == self.morpion[1][1] == self.morpion[2][1] and not self.morpion[0][1] == 0:
            # correspond à :
            # 0 X 0
            # 0 X 0
            # 0 X 0
            print('VICTORY')
            return self.morpion[0][1], (1, 4, 7)
        elif self.morpion[0][2] == self.morpion[1][2] == self.morpion[2][2] and not self.morpion[0][2] == 0:
            # correspond à :
            # 0 0 X
            # 0 0 X
            # 0 0 X
            print('VICTORY')
            return self.morpion[0][2], (2, 5, 8)
        elif self.morpion[0][0] == self.morpion[1][1] == self.morpion[2][2] and not self.morpion[0][0] == 0:
            # correspond à :
            # X 0 0
            # 0 X 0
            # 0 0 X
            print('VICTORY')
            return self.morpion[0][0], (0, 4, 8)
        elif self.morpion[2][0] == self.morpion[1][1] == self.morpion[0][2] and not self.morpion[2][0] == 0:
            # correspond à :
            # 0 0 X
            # 0 X 0
            # X 0 0
            print('VICTORY')
            return self.morpion[2][0], (6, 4, 2)

    def setVictory(self, victoryTuple) -> None:
        """
        Permet de mettre en place les paramètres de victoire
        Args:
            victoryTuple: tuple contenant la lettre du vainqueur et les coord des points gagnants
        """
        # On récupère les données envoyées par la fonction précédente
        winner = victoryTuple[0]
        pos = victoryTuple[1]
        # Définie qui a gagné
        if winner == 'X':
            winnerIcon = self.victory_X
        else:
            winnerIcon = self.victory_O
        # Change la couleur de la triplette gagnante en rouge
        self.listCase[pos[0]].selected(winnerIcon)
        self.listCase[pos[1]].selected(winnerIcon)
        self.listCase[pos[2]].selected(winnerIcon)
        # Empêche de continer à jouer
        self.canPlay = False

    def ai_plays(self, coord, selectionImage, user) -> None:
        """Permet d'interpréter les coups de l'IA
        Args:
            coord: Correspond au coup proposé par l'IA
            selectionImage: Correspond à l'image "O" ou "X" correspondant à l'IA
            user: Correspond à la lettre "O" ou "X" correspondant à l'IA
            """

        # 0 1 2
        # 3 4 5
        # 6 7 8
        if coord[0] == 0:
            self.listCase[coord[1]].selected(selectionImage)
        elif coord[0] == 1:
            self.listCase[coord[1]+3].selected(selectionImage)
        else:
            self.listCase[coord[1]+6].selected(selectionImage)
        self.morpion[coord[0]][coord[1]] = user

    def handleSelect(self, clickPos) -> None:
        """Permet de gérer la sélection du click
        et de sélectionner la case correspondante à l'emplacement du click

        Args:
            clickPos (tuple): correspond aux coordonnées du clic de la souris
        """

        # Permet de déterminer à qui il s'agit de jouer
        print("clickPos", clickPos)
        if self.turn % 2 == 0 or not self.isPlayingVsAI:
            if self.turn % 2 == 0:
                selectionImage = self.X
                user = 'X'
            else:
                selectionImage = self.O
                user = 'O'
            ###
            # Effectue les tests d'emplacements de souris
            # Colonne -> lignes
            # puis selectionne la case correspondante
            # et modifie self.morpion
            ###
            if clickPos[0] <= self.coordColumn2:
                if clickPos[1] <= self.coordColumn2:
                    # correspond à
                    # X 0 0
                    # 0 0 0
                    # 0 0 0
                    if self.morpion[0][0] == 0:
                        self.listCase[0].selected(selectionImage)
                        self.morpion[0][0] = user
                    else:
                        return
                elif clickPos[1] <= self.coordColumn3:
                    # correspond à
                    # 0 0 0
                    # X 0 0
                    # 0 0 0
                    if self.morpion[1][0] == 0:
                        self.listCase[3].selected(selectionImage)
                        self.morpion[1][0] = user
                    else:
                        return
                else:
                    # correspond à
                    # 0 0 0
                    # 0 0 0
                    # X 0 0
                    if self.morpion[2][0] == 0:
                        self.listCase[6].selected(selectionImage)
                        self.morpion[2][0] = user
                    else:
                        return

            elif clickPos[0] <= self.coordColumn3:
                if clickPos[1] <= self.coordColumn2:
                    # correspond à
                    # 0 X 0
                    # 0 0 0
                    # 0 0 0
                    if self.morpion[0][1] == 0:
                        self.listCase[1].selected(selectionImage)
                        self.morpion[0][1] = user
                    else:
                        return
                elif clickPos[1] <= self.coordColumn3:
                    # correspond à
                    # 0 0 0
                    # 0 X 0
                    # 0 0 0
                    if self.morpion[1][1] == 0:
                        self.listCase[4].selected(selectionImage)
                        self.morpion[1][1] = user
                    else:
                        return
                else:
                    # correspond à
                    # 0 0 0
                    # 0 0 0
                    # 0 X 0
                    if self.morpion[2][1] == 0:
                        self.listCase[7].selected(selectionImage)
                        self.morpion[2][1] = user
                    else:
                        return
            else:
                if clickPos[1] <= self.coordColumn2:
                    # correspond à
                    # 0 0 X
                    # 0 0 0
                    # 0 0 0
                    if self.morpion[0][2] == 0:
                        self.listCase[2].selected(selectionImage)
                        self.morpion[0][2] = user
                    else:
                        return
                elif clickPos[1] <= self.coordColumn3:
                    # correspond à
                    # 0 0 0
                    # 0 0 X
                    # 0 0 0
                    if self.morpion[1][2] == 0:
                        self.listCase[5].selected(selectionImage)
                        self.morpion[1][2] = user
                    else:
                        return
                else:
                    # correspond à
                    # 0 0 0
                    # 0 0 0
                    # 0 0 X
                    if self.morpion[2][2] == 0:
                        self.listCase[8].selected(selectionImage)
                        self.morpion[2][2] = user
                    else:
                        return
        else:
            # Correspond à la gestion des coups de l'AI
            selectionImage = self.O
            user = 'O'
            if self.canPlay and self.turn < self.maxTurn:
                if self.difficult:
                    board = self.boardConversion(user, "X")
                    aiCoord = AI_difficult.ai_turn(board)
                else:
                    ai = AI_easy.Morpion_AI_Easy(self.morpion, user)
                    aiCoord = ai.aiAnswers()
                print("AI : ", aiCoord)
                self.ai_plays(aiCoord, selectionImage, user)

        victoryCoord = self.handleVictory()
        if(victoryCoord):
            self.setVictory(victoryCoord)
        if self.turn == self.maxTurn:
            self.canPlay = False
        else:
            self.turn += 1
            print("TURN", self.turn)

    def boardConversion(self, user, ennemy) -> list:
        """
        Convertie les "O" et les "X" du plateau de jeu en
        +1 et -1 pour l'AI minimax
         """
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        # Parcours le tableau et remplace par -1 ou +1
        for i in range(3):
            for j in range(3):
                if self.morpion[i][j] == user:
                    board[i][j] = +1
                elif self.morpion[i][j] == ennemy:
                    board[i][j] = -1
        return board

    def restart(self) -> None:
        self.morpion = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.listCase = list(map(Case, self.coordonneesCasesX1, self.coordonneesCasesY1,
                                 self.coordonneesCasesX2, self.coordonneesCasesY2, [self.surf]*9))
        self.canPlay = True
        if self.maxTurn == 9:
            self.turn = 1
            self.maxTurn = 10
        else:
            self.turn = 0
            self.maxTurn = 9

    def handleDifficulty(self) -> None:
        """
        Permet de changer la difficulté de l'IA selectionnée
        """
        self.difficult = not self.difficult
        if self.difficult:
            self.surf.fill(RED)
            print("Passage en difficulté difficile ⭐⭐⭐")
        else:
            self.surf.fill(BLACK)
            print("Passage en difficulté facile ⭐")
        self.restart()

    def tutorial(self) -> None:
        self.surf.fill(WHITE)
        smallfont = pygame.font.Font(None, 30)
        welcome = smallfont.render(
            "Bienvenue sur Tic-Tac-Toe !", False, BLACK)
        returnWord = smallfont.render(
            "Appuyer sur <RETURN> pour rejouer", False, BLACK)
        changeDifficulty = smallfont.render(
            "Appuyer sur <SPACE> pour changer de difficulté", False, BLACK)
        changePvPToPvE = smallfont.render(
            "Appuyer sur <A> pour jouer à deux", False, BLACK)
        showTutorial = smallfont.render(
            "Appuyer sur <H> pour afficher ce tutoriel", False, BLACK)
        continuer = smallfont.render(
            "Appuyer sur n'importe quelle touche pour continuer", False, BLACK)
        self.surf.blit(welcome, (165, 150))
        self.surf.blit(returnWord, (110, 225))
        self.surf.blit(changePvPToPvE, (120, 260))
        self.surf.blit(changeDifficulty, (50, 295))
        self.surf.blit(showTutorial, (100, 330))
        self.surf.blit(continuer, (50, 450))

    def start(self) -> None:
        """
        Correspond à la boucle principale du jeu.
        Elle appelle la majorité des fonctions.
        Elle doit être appelée pour lancer le jeu.
        """
        run = True
        clock = pygame.time.Clock()
        pygame.font.init()
        # Fait apparaître les cases
        # de gauche à droite et de haut en bas
        # indices de self.listCase :
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.listCase = list(map(Case, self.coordonneesCasesX1, self.coordonneesCasesY1,
                                 self.coordonneesCasesX2, self.coordonneesCasesY2, [self.surf]*9))
        while run:
            clock.tick(30)
            pygame.display.flip()
            if self.showTuto:
                self.tutorial()
            else:

                # Simule le tour de l'IA
                if self.turn % 2 == 1 and self.canPlay and self.isPlayingVsAI:
                    print(f"IA PLAYS {self.turn}")
                    self.handleSelect(0)

            for event in pygame.event.get():

                # Permet de quitter le jeu
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Permet de récupérer les coordonnées du click
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        if self.canPlay and not self.showTuto:
                            clickPos = pygame.mouse.get_pos()
                            self.handleSelect(clickPos)

                if event.type == pygame.KEYDOWN:
                    if self.showTuto:
                        self.showTuto = False
                        self.surf.fill(BLACK)
                        self.restart()
                    else:
                        # Permet de changer la difficulté de l'AI
                        if event.key == pygame.K_SPACE:
                            if not self.canPlay:
                                self.handleDifficulty()
                        elif event.key == pygame.K_a:
                            # Permet de passer de PvE à PvP
                            if not self.canPlay:
                                self.isPlayingVsAI = not self.isPlayingVsAI
                        elif event.key == pygame.K_RETURN:
                            # Permet de relancer la partie
                            self.restart()
                        elif event.key == pygame.K_h:
                            self.showTuto = not self.showTuto

            pygame.display.flip()
        pygame.quit()


class Case(Morpion):
    """Correspond à une case du Morpion"""

    def __init__(self, x1: int, y1: int, x2: int, y2: int, surf) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.surf = surf
        pygame.draw.rect(self.surf, WHITE, pygame.Rect(
            self.x1, self.y1, self.x2, self.y2,))

    def selected(self, image):
        """Permet d'afficher 'X' ou 'O' en fonction de
        qui a selectionné la case."""
        self.surf.blit(image, (self.x1, self.y1))


if __name__ == "__main__":
    game = Morpion(WINDOWSIZE)
    game.start()
