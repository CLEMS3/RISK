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
        self.window = pygame.display.set_mode(size, pygame.FULLSCREEN)      # Plein écran
        pygame.display.set_caption("Risk - Game")
        self.coords = self.charger_coord_texte()

        # Taille de l'écran
        self.fen_width, self.fen_height = pygame.display.get_surface().get_size() #640, 480

        self.view = 0 #Renforcement : 0, attaque : 1, déplacement de troupe : 2, win : 3, mission : 4

        #initialisation
        self.charger_images()
        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height)
        print(len(self.game.li_territoires_obj))
        print(type(self.liste_joueurs_obj))
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions
        self.deplacement = True
        self.played_at_least_once = []

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False

                #différentes vues
                elif self.view == 0: #renforcement
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase de renforcement", True, (255, 255, 255)),(0.625*self.fen_width, 0.917*self.fen_height))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for country in self.game.li_territoires_obj:
                            try:
                                if country.mask.get_at((event.pos[0], event.pos[1])):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country.nom_territoire)
                                    print(self.select)


                            except IndexError:
                                pass
                    if len(self.select) == 2 : 
                        self.select.remove(self.select[0])
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p and len(self.select) == 1:
                            self.game.ajout_de_troupes_sur_territoires(self.a_qui_le_tour, self.get_obj(self.select[0]), 1)


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 0
                            self.view = 4
                        if event.key == pygame.K_RETURN :
                            print(self.played_at_least_once)
                            print(f"len(self.played_at_least_once) = {len(self.played_at_least_once)}")
                            print(f"len(self.liste_joueurs_obj) = {len(self.liste_joueurs_obj)}")
                            if self.a_qui_le_tour.troupe_a_repartir == 0:
                                self.select=[]
                                if len(self.played_at_least_once) >= len(self.liste_joueurs_obj)-1:
                                    self.view = 1
                                else:
                                    self.played_at_least_once.append(self.a_qui_le_tour)
                                    self.next_player()
                            else:
                                print("Il vous reste encore des troupes à répartir")


                elif self.view == 1: #attaque
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for country in self.game.li_territoires_obj:
                            try:
                                if country.mask.get_at((event.pos[0], event.pos[1])):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country.nom_territoire)
                                    print(self.select)

                            except IndexError:
                                pass

                    if self.select != [] : 
                        if self.get_obj(self.select[0]).joueur != self.a_qui_le_tour :
                            print("Vous ne pouvez pas attaquer avec un territoire qui ne vous appartient pas")
                            self.select=[]
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 1
                            self.view = 4
                        if event.type == 768 and len(self.select) == 2:
                            self.game.attaque(self.get_obj(self.select[0]), self.get_obj(self.select[1]))
                        if event.key == pygame.K_RETURN:
                            self.view = 2
                            self.select=[]

                elif self.view == 2: #déplacement
                    self.afficher_carte()
                    self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for country in self.game.li_territoires_obj:
                            try:
                                if country.mask.get_at((event.pos[0], event.pos[1])):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country.nom_territoire)
                                    print(self.select)

                            except IndexError:
                                pass
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 2
                            self.view = 4
                        if event.key == pygame.K_t and len(self.select) == 2:
                            self.game.transfert_troupes(self.get_obj(self.select[0]), self.get_obj(self.select[1]),1)
                            self.deplacement = False
                        #reverifier si le déplacement est facultatif
                        if event.key == pygame.K_RETURN :
                            self.end_turn()

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
        #arrière plan
        self.window.blit(self.bg, (0, 0))
        #territoires
        for country in self.game.li_territoires_obj:
            self.window.blit(country.surface, (0,0))
        #nombre de régiment
        for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
            self.window.blit(self.text_font.render(f"{self.get_obj(country.nom_territoire).nombre_troupes}", True, (255, 255, 255)),(self.coords[country.nom_territoire][0]*self.fen_width, self.coords[country.nom_territoire][1]*self.fen_height))#{country.nombre_troupes}
        #joueur
        self.window.blit(
            self.text_font.render(f"{self.a_qui_le_tour}", True, self.a_qui_le_tour.couleur), (0.05 * self.fen_width, 0.9 * self.fen_height))

    def select_deux_surface(self, country):
        """
        permet la sélection de deux territoires en les ajoutant à la liste select.
        On peut aussi supprimer le territoire selectionné en reclickant dessus.
        Les territoires sont stocker sous forme de str à cause d'un bug inexplicable
        """
        select = self.select
        if select== [] or (len(select) == 1 and country != select[0]):
            select.append(country)
        elif len(select) == 2 and country == select[1]:
            select = select [:-1]
        elif len(select)==1 and country == select[0]:
            select = []
        self.select = select

    def get_obj(self, str_country):
        """
        permet de récuperer l'objet territoire à partir de son nom
        """
        for country in self.game.li_territoires_obj:
            if country.nom_territoire == str_country:
                return country

    def end_turn(self):
        """
        On vérifie si le joueur a gagné, si oui, on affiche la victoire, sinon on passe au joueur suivant
        """
        self.game.bonus(self.a_qui_le_tour)
        if self.a_qui_le_tour.mission.check():
            self.view = 3
        else:
            self.next_player()
        self.deplacement = True
        self.view = 0
        self.select=[]

    def next_player(self):
        if self.liste_joueurs_obj[-1] == self.a_qui_le_tour:
            self.a_qui_le_tour = self.liste_joueurs_obj[0]
        else:
            self.a_qui_le_tour = self.liste_joueurs_obj[self.liste_joueurs_obj.index(self.a_qui_le_tour) + 1]


if __name__ == "__main__":
    import main
    temp = main.MainMenu()

    window_pg = PygameWindow((temp.WIDTH, temp.HEIGHT), temp.OUT)

    # run the main loop
    window_pg.main_loop()
    pygame.quit()



