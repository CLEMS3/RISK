import random
import asyncio
import pygame
from pygame.locals import *
import glob
from random import randint, choice
import time
import json
import Rules
import widgets


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

        #facteur de reduction
        self.fac_reduc = 1.4 ###PENSER A MODIFIER DANS FICHIER RULES 
        self.pos_reduc = (4*self.fac_reduc)/(2*self.fac_reduc -2)

        #initialisation
        self.charger_images()
        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height)
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions
        #liste couleurs
        self.colors = [(0,255,0),(255,0,0),(0,0,255),(255,255,0),(255,0,255)]

        # Sélecteur de nombres
        self.selnbr = widgets.selectNB((15, 200), 3, 2, 5)

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                #print(self.view)
                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.closebutton_rect.collidepoint(pygame.mouse.get_pos()):
                    self.init_couleurs()

                #différentes vues
                elif self.view == 0: #renforcement
                    self.afficher_fenetre()
                    self.window.blit(self.text_font.render(f"Phase de renforcement", True, (255, 255, 255)),(0.625*self.fen_width, 0.917*self.fen_height))
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # Clic sur le sélecteur ?
                        self.selnbr(pygame.mouse.get_pos())
                        self.selnbr.draw(self.window)

                        for country in self.game.li_territoires_obj:
                            try:
                                #print(event.pos)
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    print("test")
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
                    self.afficher_fenetre()
                    self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 1
                            self.view = 4

                elif self.view == 2: #déplacement
                    self.afficher_fenetre()
                    self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (400, 440))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 2
                            self.view = 4

                elif self.view == 3: #win
                    self.afficher_fenetre()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 3
                            self.view = 4

                elif self.view == 4: #mission
                    self.afficher_fenetre()
                    self.window.blit(self.text_font.render(f"Mission", True, (255, 255, 255)),(0.625*self.fen_width, 0.917*self.fen_height))
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.view = self.t


            # update the window
            pygame.display.update()

    def charger_images(self):
        """
        Charge toute les images et les transforme comme il faut, sauf les pays qui sont liés à la classe territoire
        """
        #fond d'écran
        self.bg = pygame.image.load("Images/background.jpg").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (int(self.fen_width), int(self.fen_height)))
        #fond de la map
        self.water = pygame.image.load("Images/ocean_texture.jpg").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
        self.water = pygame.transform.scale(self.water, (int(self.fen_width/(self.fac_reduc)-5), int(self.fen_height/(self.fac_reduc))))
        #adios - bouton quitter
        self.adios = pygame.image.load("Images/adios.png").convert_alpha()
        self.adios = pygame.transform.scale(self.adios,(int(self.fen_height/(self.pos_reduc)-10),int(self.fen_height/(self.pos_reduc)-10)))

    def charger_coord_texte(self):
        with open('Fichiers/coords.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues

    def afficher_fenetre(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """
        self.window.blit(self.bg,(0,0))
        self.window.blit(self.water, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        self.window.blit(self.adios,(int(self.fen_width-self.adios.get_size()[0]-5),5))
        self.add_borders()
        self.selnbr.draw(self.window)   # Dessiner le sélecteur

        
        for country in self.game.li_territoires_obj:
            self.window.blit(country.surface, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
            self.window.blit(self.text_font.render(f"{country.nombre_troupes}", True, (255, 255, 255)),(self.coords[country.nom_territoire][0]*self.fen_width/(self.fac_reduc)+2*int(self.fen_width/(self.pos_reduc)), self.coords[country.nom_territoire][1]*self.fen_height/(self.fac_reduc)+int(self.fen_height/(self.pos_reduc))))#{country.nombre_troupes}
        
    def init_couleurs(self):
       '''initialise la couleur des territoires en début de partie'''
       for country in self.game.li_territoires_obj:
            surface = country.surface
            width, height = surface.get_size()
        
            for i in range(len(self.liste_joueurs_obj)):
                if country.joueur == self.liste_joueurs_obj[i]:
                    color = self.colors[i]

            for x in range(width):
                for y in range(height):
                    if surface.get_at((x,y))!=(0,0,0):
				    


                        a = surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                        r = color[0]
                        g = color[1]
                        b = color[2]
                    
                        surface.set_at((x, y), pygame.Color(r, g, b,a)) # défini la couleur du pixel selon les valeurs de rgb données, et avec la valeur de transparence initiale
       
    def changer_lumi(self, country):
        """Assombri un territoire quand il est selectionné"""
        surface = country.surface
        width, height = surface.get_size()
        light = country.selec
        print(light)
        for x in range(width):
            for y in range(height):
                a = surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                r = surface.get_at((x, y))[0]
                g = surface.get_at((x, y))[1]
                b = surface.get_at((x, y))[2]
                
                if light == 0: #on veut assombrir l'image
                    country.selec = 1
                    #print(country.selec)
                    r = int(r/1.5)
                    g = int(g/1.5)
                    b = int(b/1.5)
                else: #on veut eclaircir l'image
                    country.selec = 0
                    r = int(r*1.5)
                    g = int(g*1.5)
                    b = int(b*1.5)
                
                surface.set_at((x, y), pygame.Color(r, g, b,a))  # défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale

    def select_deux_surface(self, country):
        """
        permet la sélection de deux territoires en les ajoutant à la liste select.
        On peut aussi supprimer le territoire selectionné en reclickant dessus.
        """
        select = self.select
        if select== [] or (len(select) == 1 and country != select[0]):
            select.append(country)
            self.changer_lumi(country)
        elif len(select) == 2 and country== select[1]:
            select = select [:-1]
            self.changer_lumi(country)
        elif len(select)==1 and country== select[0]:
            select = []
            self.changer_lumi(country)
        self.select = select

    def add_borders(self):
        #bordure autour de la map
        pygame.draw.rect(self.window, (0,0,0), (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc)),int(self.fen_width/(self.fac_reduc)-5),int(self.fen_height/(self.fac_reduc))),3)
        #bordure controles
        pygame.draw.rect(self.window, (0,0,0),(5,5, int(2*self.fen_width/(self.pos_reduc)-10),int(self.fen_height - 10)),4)
        #bordure info succes    
        pygame.draw.rect(self.window, (0,0,0),(int(2*self.fen_width/(self.pos_reduc)),5,int(self.fen_width/(self.fac_reduc)-int(self.fen_height/(self.pos_reduc))),int(self.fen_height/(self.pos_reduc)-10)),4)
        #bordure adios
        self.closebutton_rect = pygame.draw.rect(self.window, (0,0,0),(int(self.fen_width-self.adios.get_size()[0]-5),5,self.adios.get_size()[0],self.adios.get_size()[1]),3)



if __name__ == "__main__":
    import main
    menu = main.MainMenu()
    temp = menu.liste_joueurs
    out = []
    out.append(temp[0])
    out.append(temp[1])
    out.append(temp[2])
    print(out)

    window_pg = PygameWindow((menu.WIDTH, menu.HEIGHT), out)

    # run the main loop
    window_pg.main_loop()
    pygame.quit()