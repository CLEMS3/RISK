import random

import pygame
from pygame.locals import *
import glob
from random import randint, choice
import time

import Rules


class PygameWindow(pygame.Surface):
    def __init__(self, size, liste_joueurs_obj):
        super().__init__(size) #sert à éviter un problème d'héritage de classe
        pygame.init()
        self.size = size
        self.liste_joueurs_obj = liste_joueurs_obj
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption("Risk - Game")
        # Dossier des images de pays
        self.PATH_PAYS = 'Pictures/Maps/'
        # Taille de l'écran
        self.fen_width, self.fen_height = pygame.display.get_surface().get_size()
        self.liste_surface_pays = []
        self.view = 0 #Renforcement : 0, attaque : 1, déplacement de troupe : 2, win : 3, mission : 4

        #initialisation
        self.charger_carte()
        self.game = Rules.Game(self.liste_joueurs_obj)
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():

                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False

                #différentes vus
                elif self.view == 0: #renforcement
                    self.afficher_carte()

                elif self.view == 1: #attaque
                    self.afficher_carte()

                elif self.view == 2: #déplacement
                    self.afficher_carte()

                elif self.view == 3: #win
                    self.afficher_carte()

                elif self.view == 4: #mission
                    self.afficher_carte()

            # update the window
            pygame.display.update()

    def charger_carte(self):
        """
        Charge toute les images et les transforme comme il faut
        """
        pays_liste = self.liste_pays(self.PATH_PAYS, 1, 42)
        self.liste_surface_pays = []
        for cptr, pays in enumerate(pays_liste):
            image = pygame.image.load(pays).convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
            image = pygame.transform.scale(image, (int(self.fen_width), int(self.fen_height)))
            self.liste_surface_pays.append(image)
        self.bg = pygame.image.load("Images/ocean_texture.jpg").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
        self.bg = pygame.transform.scale(self.bg, (int(self.fen_width), int(self.fen_height)))


    def afficher_carte(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """
        self.window.blit(self.bg, (0, 0))
        for image in self.liste_surface_pays:
            self.window.blit(image, (0,0))


    def liste_pays(self, path_init: str, start: int, stop: int, prefix: str = ""):
        """
        Prend en argument le chemin du dossier des images des pays `path_init`,
        ainsi que la valeur initiale `start` et finale `stop` des indices dans les noms.
        Admet aussi un argument optionnel `prefix` pour les noms des pays, tel que <prefix><indice>.png

        Renvoie une liste de strings contenant les chemins des pays à afficher
        """
        out = []

        for cptr in range(start, stop + 1):
            text = path_init + prefix + str(cptr) + ".png"
            out.append(str(text))

        return out

    def changer_couleur(self, surface, color):
        """Remplace tous les pixels de la surface avec color, garde la transparence"""
        width, height = surface.get_size()
        r, g, b = color
        for x in range(width):
            for y in range(height):
                a = surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                surface.set_at((x, y), pygame.Color(r, g, b,a))  # défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale