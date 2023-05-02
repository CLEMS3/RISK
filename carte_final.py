import random

import pygame
from pygame.locals import *
import glob
from random import randint, choice
import time
import json

import Rules


class PygameWindow(pygame.Surface):
    def __init__(self, size, liste_joueurs_obj):
        super().__init__(size) #sert à éviter un problème d'héritage de classe
        pygame.init()
        self.size = size
        self.liste_joueurs_obj = liste_joueurs_obj
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption("Risk - Game")
        self.coords = self.charger_coord_texte()

        # Taille de l'écran
        self.fen_width, self.fen_height = pygame.display.get_surface().get_size() #640, 480
        self.view = 0 #Renforcement : 0, attaque : 1, déplacement de troupe : 2, win : 3, mission : 4

        #initialisation
        self.charger_images()
        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height)
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                print(self.view)
                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False

                #différentes vus
                elif self.view == 0: #renforcement
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase de renforcement", True, (255, 255, 255)),(400, 440))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for country in self.game.li_territoires_obj:
                            try:
                                if country.mask.get_at((event.pos[0], event.pos[1])):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
                                    print(self.select)
                            except IndexError:
                                pass
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 0
                            self.view = 4


                elif self.view == 1: #attaque
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 1
                            self.view = 4

                elif self.view == 2: #déplacement
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 2
                            self.view = 4

                elif self.view == 3: #win
                    self.afficher_carte()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 3
                            self.view = 4

                elif self.view == 4: #mission
                    self.afficher_carte()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.view = self.t


            # update the window
            pygame.display.update()

    def charger_images(self):
        """
        Charge toute les images et les transforme comme il faut, sauf les pays qui sont liés à la classe territoire
        """
        self.bg = pygame.image.load("Images/ocean_texture.jpg").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
        self.bg = pygame.transform.scale(self.bg, (int(self.fen_width), int(self.fen_height)))

    def charger_coord_texte(self):
        with open('Fichiers/coords.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues

    def afficher_carte(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """
        self.window.blit(self.bg, (0, 0))
        for country in self.game.li_territoires_obj:
            self.window.blit(country.surface, (0,0))
        for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
            self.window.blit(self.text_font.render(f"{country.nombre_troupes}", True, (255, 255, 255)),tuple(self.coords[country.nom_territoire]))#{country.nombre_troupes}


    def changer_couleur(self, surface, color):
        """Remplace tous les pixels de la surface avec color, garde la transparence"""
        width, height = surface.get_size()
        r, g, b = color
        for x in range(width):
            for y in range(height):
                a = surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                surface.set_at((x, y), pygame.Color(r, g, b,a))  # défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale

    def select_deux_surface(self, country):
        """
        permet la sélection de deux territoires en les ajoutant à la liste select.
        On peut aussi supprimer le territoire selectionné en reclickant dessus.
        """
        select = self.select
        if select== [] or (len(select) == 1 and country != select[0]):
            select.append(country)
        elif len(select) == 2 and country == select[1]:
            select = select [:-1]
        elif len(select)==1 and country == select[0]:
            select = []
        self.select = select
