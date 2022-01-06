#!/usr/bin/env python3
from random import randint
"""
AI qui lit les coups sur le moment sans faire de potentielle prédiction.
Elle choisit le meilleur coup à partir d'un tableau de coordonnés
correspondant au morpion, elle attribue un score à chaque case pour
déterminer quel est son meilleur mouvement.

Difficulté : ⭐
Motif : Aucune prédiction, battable avec la même technique


"""


class Morpion_AI_Easy:
    def __init__(self, state: list, player) -> None:
        self.morpion = state

        if player == "O":
            self.ennemy = 'X'
        else:
            self.ennemy = "O"

        self.player = player

    def testRow(self) -> tuple:
        """Permet d'attribuer un score à toutes les cases en lecture par ligne"""
        bestRowCoord = []
        bestPoints = 0
        for ligne in range(len(self.morpion)):
            tmpCaseCoordFree = []
            tmpCaseSelectedFriendlyNb = 0
            tmpCaseSelectedEnnemyNb = 0
            for case in range(len(self.morpion)):
                # Ajoute dans la liste les cases libres
                if self.morpion[ligne][case] == 0:
                    tmpCaseCoordFree.append((ligne, case))

                if self.morpion[ligne][case] == self.player:
                    tmpCaseSelectedFriendlyNb += 1
                elif self.morpion[ligne][case] == self.ennemy:
                    tmpCaseSelectedEnnemyNb += 1
            rowPoints = self.scoreTesting(
                tmpCaseSelectedFriendlyNb, tmpCaseSelectedEnnemyNb)
            if bestPoints < rowPoints:
                bestPoints = rowPoints
                bestRowCoord = tmpCaseCoordFree
        return bestRowCoord, bestPoints

    def testColumn(self):
        """Permet d'attribuer un score à toutes les cases en lecture par colonne"""
        bestColumnCoord = []
        bestPoints = 0
        for case in range(len(self.morpion)):
            tmpCaseCoordFree = []
            tmpCaseSelectedFriendlyNb = 0
            tmpCaseSelectedEnnemyNb = 0
            for colonne in range(len(self.morpion)):
                if self.morpion[colonne][case] == 0:
                    tmpCaseCoordFree.append((colonne, case))

                if self.morpion[colonne][case] == self.player:
                    tmpCaseSelectedFriendlyNb += 1
                elif self.morpion[colonne][case] == self.ennemy:
                    tmpCaseSelectedEnnemyNb += 1

            columnPoints = self.scoreTesting(
                tmpCaseSelectedFriendlyNb, tmpCaseSelectedEnnemyNb)
            if bestPoints < columnPoints:
                bestPoints = columnPoints
                bestColumnCoord = tmpCaseCoordFree
        return bestColumnCoord, bestPoints

    def testDiagonal(self):
        """Permet d'attribuer un score à toutes les cases par lecture diagonale"""
        #  0 0 1 2
        #  1 0 1 2
        #  2 0 1 2
        bestPoints = 0
        sens = 0
        bestCoord = []
        for _ in range(2):
            tmpCaseCoordFree = []
            tmpCaseSelectedFriendlyNb = 0
            tmpCaseSelectedEnnemyNb = 0
            for x in range(3):
                if self.morpion[x][abs(sens-x)] == 0:
                    tmpCaseCoordFree.append((x, abs(sens-x)))
                if self.morpion[x][abs(sens-x)] == self.player:
                    tmpCaseSelectedFriendlyNb += 1
                elif self.morpion[x][abs(sens-x)] == self.ennemy:
                    tmpCaseSelectedEnnemyNb += 1
            diagonalPointPoints = self.scoreTesting(
                tmpCaseSelectedFriendlyNb, tmpCaseSelectedEnnemyNb)
            if bestPoints < diagonalPointPoints:
                bestPoints = diagonalPointPoints
                bestCoord = tmpCaseCoordFree
            sens = 2
        return bestCoord, bestPoints

    def aiAnswers(self):
        # Meilleur décision pour les victoires lignes

        bestRowCoord, bestRowPoints = self.testRow()
        bestColumnCoord, bestColumnPoints = self.testColumn()
        bestDiagonalCoord, bestDiagnonalPoints = self.testDiagonal()
        # Meilleur décision pour les victoires colonnes

        # print(bestRowCoord, bestColumnPoints)
        # print(bestColumnCoord, bestColumnPoints)
        # print(bestDiagonalCoord, bestDiagnonalPoints)
        coord = 0
        if bestRowPoints >= bestColumnPoints and bestRowPoints >= bestDiagnonalPoints and len(bestRowCoord) > 0:
            coord = bestRowCoord[randint(0, len(bestRowCoord)-1)]
        elif bestColumnPoints >= bestDiagnonalPoints and bestColumnPoints > bestRowPoints and len(bestColumnCoord) > 0:
            coord = bestColumnCoord[randint(0, len(bestColumnCoord)-1)]
        else:
            if len(bestDiagonalCoord) > 0:
                print(bestDiagonalCoord[0])
                coord = bestDiagonalCoord[randint(0, len(bestDiagonalCoord)-1)]
        return coord

    def scoreTesting(self, caseFriendly, caseEnnemy):
        if caseFriendly == 1 and caseEnnemy == 0:
            rowPoints = 30
        elif caseFriendly == 1 and caseEnnemy == 1:
            rowPoints = 10
        elif caseEnnemy == 2 and caseFriendly == 0:
            rowPoints = 100
        elif caseFriendly == 2 and caseEnnemy == 0:
            rowPoints = 1000
        else:
            rowPoints = 1
        return rowPoints


if __name__ == "__main__":
    morpionState = [
        ["X", "O", 0],
        ["X", 0, 0],
        [0, 0, 0]
    ]
    morpionAI = Morpion_AI_Easy(morpionState, "O")
    print(morpionAI.aiAnswers())
