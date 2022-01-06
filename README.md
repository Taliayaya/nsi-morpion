# Nsi Morpion

## Introduction

Nsi Morpion est un miniprojet de NSI consistant à reproduire le jeu du morpion, aussi appelé Tic-Tac-Toe, en python à l'aide du module pygame.

## Jouer au jeu

### Présentation

Ce jeu de morpion a été recréé de deux manières très distinctes :

-   L'original
-   La Revisité

En effet, la première version représente le Morpion basique que l'on connait tous. Un plateau de 9 cases dans lequel s'affronte les `"O"` et les `"X"` dans le but d'aligner 3 de leurs pions. <br/>
Ce mode jeu propose deux IA contre lequel l'utilisateur peut jouer.

La deuxième version, quant-à elle, est une version revisité du jeu de Morpion. Contrairement à l'original, il est possible de s'affronter sur un plateau dont le nombre de case peut varier, tout comme les conditions de victoire. <br/>
Ces paramètres sont modifiables par l'utilisateur, offrant une grande diversité dans les parties, pour un plaisir infini.

### Télécharger le code source

Le code source du jeu est hébergé par GitHub. Il est donc téléchargeable depuis `Git` ou en exportation `.zip`

#### Télécharger par Git

Copier la commande suivante et depuis le terminal, l'exécuter depuis le dossier parent souhaité.

```bash
$ git clone https://github.com/Taliayaya/nsi-morpion
```

Cela créera le dossier nsi-morpion dans votre répertoire courant.

#### Exécuter le code

Il existe plusieurs fichiers dans ce projet. Parmis eux, `main.py` et `MorpionNSIV2.py`.

-   `main.py` correspond au Morpion "Original"
-   `MorpionNSIV2.py` correspond au Morpion "Revisité".

Vous pouvez les exécuter de plusieurs façon différentes.

-   Depuis le Terminal
    -   Avec python
    ```bash
    $ python3 main.py
    $ python3 MorpionNSIV2.py
    ```
    -   Sur Linux
    ```bash
    $ chmod +x main.py MorpionNSIV2.py
    $ ./main.py
    $ ./MorpionNSIV2.py
    ```
-   Depuis un IDE
    -   Le programme se lance par n'importe quel IDE.
    -   Le programme se lance lors d'un double clic ou de l'exécution du fichier.

> Il est important de noter que Python 3 doit être installé pour faire fonctionner ces programmes.

### Comment jouer

#### Version original (`main.py`)

Dans cette version, le jeu se joue à la souris. A tour de rôle, un utilisateur joue un coup. Un coup se joue en selectionannt une case à l'aide du clic gauche de la souris sur une case vide.
