import pygame   #importation des modules
import random

couleurs = [    #définition des variables globales : 7 couleurs
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:   #La partie Figure
    x = 0       #On dénifit le repère
    y = 0

    figures = [     #7 figures dans la matrice (voir diapo)
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):   #position initiale
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)    #forme aléatoire
        self.color = random.randint(1, len(couleurs) - 1)       #couleur aléatoire
        self.rotation = 0

    def image(self):        #On définit ce qu'est une image
        return self.figures[self.type][self.rotation]

    def rotate(self):       #On définit ce qu'est une rotation
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:       #La partie Tetris
    level = 2       #Les variables locales...
    score = 0
    state = "start"
    field = []
    x = 100
    y = 60
    zoom = 20
    hauteur = 0
    largeur = 0
    figure = None

    def __init__(self, hauteur, largeur):       #L'interface initial
        self.height = hauteur
        self.width = largeur
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(hauteur):        #Boucle for avec les indentations pour la hauteur
            new_line = []
            for j in range(largeur):        #Boucle for avec les indentations pour la largeur
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):       #Définition d'une nouvelle figure
        self.figure = Figure(3, 0)

    def intersects(self):       #Définition d'une intersection (plus détaillé dans la diapo)
        intersection = False
        for i in range(4):      #Boucle for avec les indentations
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):      #Définition de la destructions des lignes
        lignes = 0
        for i in range(1, self.height):     #Boucle for avec les indentations pour la hauteur
            zeros = 0
            for j in range(self.width):     #Boucle for avec les indentations pour la largeur
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lignes += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lignes ** 2       #Score = [lignes cassées]²

    def go_space(self):     #Définition des déplacement dans l'espace
        while not self.intersects():        #Boucle while not avec les indentations
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):      #Définition des déplacement vers le bas
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):       #Définition du gèle
        for i in range(4):      #Boucle for avec les indentations
            for j in range(4):
                if i * 4 + j in self.figure.image():        #Image = ce qu'il reste dans le champs
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "game over"

    def go_side(self, dx):      #Définition du déplacement vers sur le côté
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x       #anciennes coordonnées

    def rotate(self):       #Définition d'une rotation
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation     #ancienne rotation


pygame.init()       # Initialisation du moteur de jeu (IDE)

NOIR = (0, 0, 0)        # Définition de 3 couleurs
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)

size = (400, 500)       #paramétrage de l'écran
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")        #titre de la fenêtre

# Boucle jusqu'à ce que l'utilisateur clique sur le bouton de fermeture.
done = False
clock = pygame.time.Clock()     #introduction d'une notion de temps
fps = 25
game = Tetris(20, 10) 	   #dimensions de la grille
counter = 0

pressing_down = False       #Chute des pièces

while not done:     #Boucle while not
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:  #On ne dépasse pas un score > 100 000 (même si c'est impossible de l'atteindre, par sécurité)
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:        #vittesse de descente du jeu
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():        #boucle d'évènement for avec les intendations pour gérer les itérateurs et l'interface entre le clavier et le programme
        if event.type == pygame.QUIT:       #Si on quitte pygame = fin
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:       #Flèche du haut
                game.rotate()
            if event.key == pygame.K_DOWN:       #Flèche du bas
                pressing_down = True
            if event.key == pygame.K_LEFT:       #Flèche de gauche
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:       #Flèche de droite
                game.go_side(1)
            if event.key == pygame.K_SPACE:     #Barre d'espace
                game.go_space()
            if event.key == pygame.K_ESCAPE:        #Touche échap, on reinitialise la hauteur et la largeur
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLANC)      #arrière plan blanc
#paramétrage du quadrillage
    for i in range(game.height):      #Boucle for avec les indentations pour la hauteur
        for j in range(game.width):      #Boucle for avec les indentations pour la largeur
            pygame.draw.rect(screen, GRIS, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:        #les lignes sont grises
                pygame.draw.rect(screen, couleurs[game.field[i][j]],        #le fond est de la couleur du champ
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:     #Paramétrage de la figure dans le quadrillage
        for i in range(4):      #Boucle for avec les indentations
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():    #on définit les couleurs là ou il y a une forme/figure
                    pygame.draw.rect(screen, couleurs[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)      #Intruduction des fonctions d'affichage du texte
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, NOIR)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])       #Paramètre d'affichage des foctions si c'est game over
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()       #fin des modules
    clock.tick(fps)

pygame.quit()       #désinstallation de l'IDE
