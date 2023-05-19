import random
import asyncio
import pygame
from pygame.locals import *
import glob
from random import randint, choice, shuffle
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
        self.fac_reduc = 1.5 ###PENSER A MODIFIER DANS FICHIER RULES 

        self.pos_reduc = (4*self.fac_reduc)/(2*self.fac_reduc -2)

        #initialisation
        self.charger_images()
        self.display_dice = True
        self.dice_list = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5] #pour l'affichage random des dés, plusieurs fois 1-6 pour avoir plus de variété

        # Barre de texte pour les messages
        self.barre_texte = widgets.barreTexte(self.window, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.fac_reduc))+5), self.water.get_size()[0], 30)
        self.barre_texte.changer_texte(["Bonjour ! Ceci est une barre de texte pour afficher des messages."])

        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height, self.barre_texte)
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.text_font_big = pygame.font.Font("Fonts/ARLRDBD.TTF", 50)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions
        self.deplacement = True
        self.placement_initial = []
        self.tour_initial = []

        #liste couleurs
        self.colors = [(174,160,75),(198,166,100),(230,214,144),(190,189,127),(228,160,16),(225,204,79)]

        # Sélecteur de nombres
        self.init_couleurs()
        
        self.selnbr_des1 = widgets.selectNB((15, int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+100), 1, 1, 3) #nombre de dés => affichage du bon nombre de dés en fonction de la selection 
        self.selnbr_des2 = widgets.selectNB((15, int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+170), 1, 1, 2) 


    def main_loop(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.closebutton_rect.collidepoint(pygame.mouse.get_pos()):
                    running = False

                #différentes vues
                elif self.view == 0: #renforcement
                    self.afficher_fenetre()
                    self.display_dice = False
                    nbr_restant = self.a_qui_le_tour.troupe_a_repartir
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        #clic sur bouton +
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90)), int(event.pos[1]-int(self.fen_height/(self.pos_reduc)))) #pour verifier si souris sur bouton sur le mask
                            if  self.plus_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour:
                                    if nbr_restant > 0:           #TODO  rajouter des messages d'erreur pour quand les troupes sont plus suffisantes ou le territoire n'appartient pas a celui qui joue 
                                        print("plus")
                                        self.select[0].nombre_troupes += 1 #ajout de la troupe sur le pays
                                        self.a_qui_le_tour.troupe_a_repartir -= 1 #retrait d'une troupe dans la liste des troupes a ajouter
                                    else :  self.barre_texte.changer_texte(["Vous n'avez plus de troupes à répartir."], err=True, forceupdate=True)
                                else:
                                    self.barre_texte.changer_texte(["Ce territoire ne vous appartient pas."], err=True, forceupdate=True)
                        except IndexError: pass
                        #clic sur bouton -
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) +30)), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                            if  self.minus_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour:
                                    if self.select[0].nombre_troupes > self.game.nb_troupes_minimum[self.select[0].nom_territoire]:
                                        print("moins")
                                        self.select[0].nombre_troupes -= 1
                                        self.a_qui_le_tour.troupe_a_repartir += 1
                                    else :  self.barre_texte.changer_texte([f"Vous ne pouvez pas avoir moins de {self.game.nb_troupes_minimum[self.select[0].nom_territoire]} troupes sur ce territoire."], err=True, forceupdate=True)
                                else:
                                    self.barre_texte.changer_texte(["Ce territoire ne vous appartient pas."], err=True, forceupdate=True)
                        except IndexError: pass 
                        
                       
                        #clic sur pays
                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
    
                            except IndexError:
                                pass
                        

                        #clic sur next
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                        
                                #si toutes les troupes sont placées
                                if self.a_qui_le_tour.troupe_a_repartir == 0:
                                    self.changer_lumi(self.select[0])
                                    self.select.remove(self.select[0])
                                    if len(self.placement_initial) >= len(self.liste_joueurs_obj)-1:
                                        self.view = 1
                                    else: #si tous les joueurs ont placé leurs troupes
                                        self.placement_initial.append(self.a_qui_le_tour)
                                        self.next_player()
                                else:
                                    self.barre_texte.changer_texte(["Il vous reste encore des troupes à répartir"], err=True, forceupdate=True)
                        except IndexError : pass 
                    
                    #selection d'un seul pays dans la phase de renforcement         
                    if len(self.select) == 2 : 
                        self.changer_lumi(self.select[0])
                        self.select.remove(self.select[0])

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 0
                            self.view = 4
                    
                elif self.view == 1: #attaque
                    self.afficher_fenetre()
                    self.display_dice = True
                    try : self.selnbr_troupes = widgets.selectNB((15, int(self.fen_height/(self.pos_reduc))+(int(self.fen_height/(self.pos_reduc)-10))/2), 1, 1, self.select[0].nombre_troupes)  
                    except: self.selnbr_troupes = widgets.selectNB((15, int(self.fen_height/(self.pos_reduc))+(int(self.fen_height/(self.pos_reduc)-10))/2), 1, 1, 1)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        #TODO ajouter un widget(nombre de dés du joueur attaqué)
                        #selecteur nombre de regiment
                        #TODO changer l'ordre ou ça blit pour pas qu'il y a une sperposition bizzare
                        if self.selnbr_troupes(pygame.mouse.get_pos()) == 0:
                            self.selnbr_troupes.increment()
                        elif self.selnbr_troupes(pygame.mouse.get_pos()) == 1:
                            self.selnbr_troupes.decrement()
                        self.selnbr_troupes.draw(self.window)

                        #selecteur nombre de dés 1 : attaque
                        if self.selnbr_des1(pygame.mouse.get_pos()) == 0:
                            self.selnbr_des1.increment()
                            shuffle(self.dice_list) #change les faces de dés affichées
                        elif self.selnbr_des1(pygame.mouse.get_pos()) == 1:
                            self.selnbr_des1.decrement()
                            shuffle(self.dice_list) #change les faces de dés affichées
                        self.selnbr_des1.draw(self.window)

                        #selecteur nombre de dés 2 : défence
                        if self.selnbr_des2(pygame.mouse.get_pos()) == 0:
                            self.selnbr_des2.increment()
                        elif self.selnbr_des2(pygame.mouse.get_pos()) == 1:
                            self.selnbr_des2.decrement()
                        self.selnbr_des2.draw(self.window)

                        #check clic sur pays
                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
                                    

                            except IndexError:
                                pass
                        print(event.pos)
                        print(self.fen_height)
                        #clic sur "Attaque"
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-150),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                if len(self.select) == 2:
                                    print("attaque")
                                    print(f"nombre de troupes : {self.selnbr_troupes.etat}")
                                    print(f"nombre de des attaque : {self.selnbr_des1.etat}")
                                    print(f"nombre de des defence : {self.selnbr_des2.etat}")
                                    self.game.attaque(self.select[0], self.select[1], self.selnbr_troupes.etat, self.selnbr_des1.etat, self.selnbr_des2.etat) 
                                    self.empty_select()
                                    #AJOUTER MESSAGE ERREUR SUR BARRE VITTO > voir rules.py
                                    # à adapter
                        except IndexError : pass

                        #clic sur next, 
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                self.view = 2
                                self.barre_texte.changer_texte(["Fin de la phase d'attaque"], err=True, forceupdate=True)
                                self.empty_select()

                        except IndexError : pass

                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            self.barre_texte.changer_texte(["Vous ne pouvez pas attaquer avec un territoire qui ne vous appartient pas"], err=True, forceupdate=True)
                            

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 1
                            self.view = 4

                elif self.view == 2: #déplacement
                    self.afficher_fenetre()
                    self.display_dice = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :

                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
                            except IndexError:
                                pass

                        #clic sur next, à voir si deplacement obligatoire
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                self.barre_texte.changer_texte(["Fin de la phase de déplacement"], err=True, forceupdate=True)
                                self.end_turn()
                        except IndexError : pass

                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-150),event.pos[1]-(self.fen_height-80))
                            if self.transfert_mask.get_at(scaled_pos):
                                if len(self.select) == 2:
                                    self.game.transfert_troupes(self.select[0], self.select[1],1)
                                    self.deplacement = False
                                    #VITTO VOIR POUR MESSAGE D'ERREUR SI NON ADJACENT
                        except IndexError : pass

                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            self.barre_texte.changer_texte(["Vous ne pouvez pas transférer des troupes depuis un territoire qui ne vous appartient pas"], err=True, forceupdate=True)
                            
                        if len(self.select)==2 and self.select[1].joueur != self.a_qui_le_tour :
                            self.barre_texte.changer_texte(["Vous ne pouvez pas transférer des troupes à un territoire qui ne vous appartient pas"], err=True, forceupdate=True)
                            
                    
                       
                elif self.view == 3: #win
                    self.afficher_fenetre()
                    self.window.blit(self.ecran_victoire, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
                    self.display_dice = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 3
                            self.view = 4

                elif self.view == 4: #mission
                    self.afficher_fenetre()
                    self.window.blit(self.text_font.render(f"Mission", True, (255, 255, 255)),(0.625*self.fen_width, 0.917*self.fen_height))
                    self.window.blit(self.text_font.render(f"{self.a_qui_le_tour.mission.detail}", True, (0, 0, 0)),(int(0.375*self.fen_width), int(0.200*self.fen_height+20)))
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
        self.water = pygame.image.load("Images/fond_carte_3.jpg").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
        self.water = pygame.transform.scale(self.water, (int(self.fen_width/(self.fac_reduc)-5), int(self.fen_height/(self.fac_reduc))))
        #lines adjacent + nom
        self.lines = pygame.image.load("Pictures/Risk_lines.png").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
        self.lines = pygame.transform.scale(self.lines, (int(self.fen_width/(self.fac_reduc)-5), int(self.fen_height/(self.fac_reduc))))
        #adios - bouton quitter
        self.adios = pygame.image.load("Images/adios.png").convert_alpha()
        self.adios = pygame.transform.scale(self.adios,(int(self.fen_height/(self.pos_reduc)-10),int(self.fen_height/(self.pos_reduc)-10)))
        #dés
        self.dice = []
        for i in range(1,7):
            dice = pygame.image.load(f"Pictures/Dice/{i}.png")
            dice = pygame.transform.scale(dice, (60, 60))
            self.dice.append(dice)
        #boutons + et -
        self.plus = pygame.image.load("Pictures/plus.png").convert_alpha()
        self.plus = pygame.transform.scale(self.plus,(55,60))
        self.plus_mask = pygame.mask.from_surface(self.plus)
        self.minus = pygame.image.load("Pictures/minus.png").convert_alpha()
        self.minus = pygame.transform.scale(self.minus,(55,60))
        self.minus_mask = pygame.mask.from_surface(self.minus)
        #bouton next
        self.next = pygame.image.load("Pictures/next.png").convert_alpha()
        self.next = pygame.transform.scale(self.next,(50,50))
        self.next_mask = pygame.mask.from_surface(self.next)
        #bouton attaque
        self.attack = pygame.image.load("Pictures/attack.png").convert_alpha()
        self.attack = pygame.transform.scale(self.attack,(50,50))
        self.attack_mask = pygame.mask.from_surface(self.attack)
        #bouton transfert
        self.transfert = pygame.image.load("Pictures/transfert.png").convert_alpha()
        self.transfert = pygame.transform.scale(self.transfert,(50,50))
        self.transfert_mask = pygame.mask.from_surface(self.transfert)
        self.ecran_victoire = pygame.image.load("Images/ecran_victoire.jpg").convert_alpha()
        self.ecran_victoire = pygame.transform.scale(self.ecran_victoire, (int(self.fen_width/(self.fac_reduc)-5), int(self.fen_height/(self.fac_reduc))))



    def charger_coord_texte(self):
        with open('Fichiers/coords.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues

    def afficher_fenetre(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """

        #bg
        self.window.blit(self.bg,(0,0))
        if self.view not in [3,4]: #pas de carte pour les fenetres win et mission
            self.window.blit(self.water, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
            self.window.blit(self.lines, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        self.window.blit(self.adios,(int(self.fen_width-self.adios.get_size()[0]-5),5))
        self.window.blit(self.next,(int(self.fen_width-80),int(self.fen_height-80)))
        self.barre_info = self.add_borders() #ajoute les bordures noires
        self.barre_info.changer_texte(["Test !", "ligne 2", "ligne 3", "ligne 4"])
        self.add_texts() #ajoute les texts
        if self.view == 0: #renforcement
            #affichage boutons + et - (juste pendant renforcement)
            self.window.blit(self.plus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90,int(self.fen_height/(self.pos_reduc))))
            self.window.blit(self.minus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) +30 ,int(self.fen_height/(self.pos_reduc))))
        elif self.view == 1: #attaque
            self.selnbr_des1.draw(self.window)   # Dessiner le sélecteur du nombre de dés d'attaque
            self.selnbr_des2.draw(self.window)   # Dessiner le sélecteur du nombre de dés de defence
            self.selnbr_troupes.draw(self.window)   # Dessiner le sélecteur du nombre de troupes
            self.affiche_des1(self.selnbr_des1.etat) # met à jour les dés

            #affichage icone attaque
            self.window.blit(self.attack,(int(self.fen_width-150),int(self.fen_height-80)))

        elif self.view == 2: #deplacement
            self.window.blit(self.transfert,(int(self.fen_width-150),int(self.fen_height-80)))

        if self.view not in [3, 4]:  # pas de carte pour les fenetres win et mission
            #territoires
            for country in self.game.li_territoires_obj:
                self.window.blit(country.surface, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
            #régiments
            for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
                self.window.blit(self.text_font.render(f"{country.nombre_troupes}", True, (0, 0, 0)),(self.coords[country.nom_territoire][0]*self.fen_width/(self.fac_reduc)+2*int(self.fen_width/(self.pos_reduc)), self.coords[country.nom_territoire][1]*self.fen_height/(self.fac_reduc)+int(self.fen_height/(self.pos_reduc))))#{country.nombre_troupes}


    def affiche_des1(self, valeur): #ATTAQUE
        '''affiche le nombre de dés nécésaires selon le choix du joueur, affiche une valeur aléatoire'''
        if self.view == 1 :
            x = int((2*self.fen_width/(self.pos_reduc)-10)/2) - 150 #pour centrer les 3 dés
            y =int(0.602*self.fen_height) +30
            pos = [(x,y),(x+120, y),(x+240,y)] #écart de 120pixel entre les x (60 entre chaque dés) 
            for i in range(valeur): 
                self.window.blit(self.dice[self.dice_list[i]],pos[i]) #affiche une face du dé aléatoire


    def init_couleurs(self):
       '''
       initialise la couleur des territoires en début de partie
       avec les mask 
       '''
       for country in self.game.li_territoires_obj:
            
            for i in range(len(self.liste_joueurs_obj)): #associe une couleur à un joueur
                if country.joueur == self.liste_joueurs_obj[i]: 
                    color = self.colors[i]
                    country.color = color 

            surface_mask = country.mask #recupere le mask du pays
            #turn mask to surface
            new_surface = surface_mask.to_surface() #creer une surface noir et blanc depuis le mask (noir = pixel vide, blanc = pixel utilisé)
            new_surface.set_colorkey((0,0,0)) #efface le noir
            new_surface.fill(color, special_flags=pygame.BLEND_RGBA_MULT)


            country.surface = new_surface

    def changer_lumi(self, country):
        """
        Assombri un territoire quand il est selectionné
        Vas recuperer la couleur du pays, si il faut assombrir, on divise la valeur r g b par 1,5 
        pour eclaircir on multiplie par 1,5
        on enregistre ensuite la nouvelle couleur du pays, modifie l'état "selec" 1= selectionné, 0= non selec

        utilise la meme methode que init_couleur pour changer la couleur du pays
        
        """
        surface = country.surface
        width, height = surface.get_size()
        light = country.selec #recupere l'etat du pays (selec ou non)
        
        r,g,b = country.color
        
        if light == 0: #on veut assombrir l'image
            country.selec = 1
            
            r = int(r/1.5)
            g = int(g/1.5)
            b= int(b/1.5)
            
            country.color = (r,g,b)
        elif light==1: #on veut eclaircir l'image
            country.selec = 0
            r = int(r*1.5)
            g = int(g*1.5)
            b = int(b*1.5)
            country.color = (r,g,b)
        surface_mask = country.mask #recupere le mask du pays
        #turn mask to surface
        new_surface = surface_mask.to_surface() #creer une surface noir et blanc depuis le mask (noir = pixel vide, blanc = pixel utilisé)
        new_surface.set_colorkey((0,0,0)) #efface le noir
        new_surface.fill((r,g,b), special_flags=pygame.BLEND_RGBA_MULT)
        country.surface = new_surface
        
    def changer_couleur(self,country,color):
        '''change la couleur du territoire avec la couleur entrée en parametre sous la forme (r,g,b)'''
        surface_mask = country.mask #recupere le mask du pays
        #turn mask to surface
        new_surface = surface_mask.to_surface() #creer une surface noir et blanc depuis le mask (noir = pixel vide, blanc = pixel utilisé)
        new_surface.set_colorkey((0,0,0)) #efface le noir
        new_surface.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    def select_deux_surface(self, country):
        """
        permet la sélection de deux territoires en les ajoutant à la liste select.
        On peut aussi supprimer le territoire selectionné en reclickant dessus.
        Les territoires sont stocker sous forme de str à cause d'un bug inexplicable
        """
        select = self.select
        if select== [] or (len(select) == 1 and country != select[0]):
            select.append(country)
            self.changer_lumi(country)
        elif len(select) == 2 and country== select[1]:
            select = select [:-1]
            self.changer_lumi(country)
        elif len(select)==1 and country== select[0]:
            self.select= []
            self.empty_select
        self.select = select

    def end_turn(self):
        """
        On vérifie si le joueur a gagné, si oui, on affiche la victoire, sinon on passe au joueur suivant
        """
        self.game.bonus(self.a_qui_le_tour)
        if len(self.tour_initial) <= 3:
            self.tour_initial.append(self.a_qui_le_tour)
        if self.a_qui_le_tour.mission.check():
            self.view = 3
        else:
            self.next_player()
        self.deplacement = True
        self.view = 0 if self.a_qui_le_tour in self.tour_initial else 1
        if self.view == 0 : 
            for territoire in self.game.li_territoires: 
                self.game.nb_troupes_minimum[territoire]=self.game.get_territoire_object(territoire).nombre_troupes
        self.empty_select()

    def empty_select(self):
        """vide self.select et deselectionne les pays"""
        for country in self.select:
            self.changer_lumi(country)
        self.select = []

    def next_player(self):
        '''passe au joueur suivant dans la partie'''
        if self.liste_joueurs_obj[-1] == self.a_qui_le_tour:
            self.a_qui_le_tour = self.liste_joueurs_obj[0]
        else:
            self.a_qui_le_tour = self.liste_joueurs_obj[self.liste_joueurs_obj.index(self.a_qui_le_tour) + 1]

    def add_borders(self):
        #bordure autour de la map
        pygame.draw.rect(self.window, (0,0,0), (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc)),int(self.fen_width/(self.fac_reduc)-5),int(self.fen_height/(self.fac_reduc))),3)
        #bordure controles
        pygame.draw.rect(self.window, (0,0,0),(5,5, int(2*self.fen_width/(self.pos_reduc)-10),int(self.fen_height - 10)),4)
        #bordure info succes
        barre_info = widgets.barreTexte(self.window, (0.333*self.fen_width, 0.0053*self.fen_height), self.water.get_size()[0] - self.adios.get_size()[0] - 3, self.fen_height*0.159, epaisseur=4, couleur_contour=(0,0,0), police=27)
        #bordure adios
        self.closebutton_rect = pygame.draw.rect(self.window, (0,0,0),(int(self.fen_width-self.adios.get_size()[0]-5),5,self.adios.get_size()[0],self.adios.get_size()[1]),3)
        if self.view == 1:  #si phase attaque
            #bordure dés
            pygame.draw.rect (self.window, (0,0,0), (int((2*self.fen_width/(self.pos_reduc)-10)/2) - 180, int(0.602*self.fen_height), int(0.23*self.fen_width), int(0.139*self.fen_height)),4) 

        return barre_info

    def add_texts(self):
        '''ajoute tous les textes necessaires durant la partie'''
        #Nom du joueur en haut de la partie controle
        nom_joueur = self.a_qui_le_tour.nom #va chercher à qui le tour
        i = self.liste_joueurs_obj.index(self.a_qui_le_tour)
        color = self.colors[i] #recupere la couleur associée au joueur
        len_name = len(nom_joueur)
        xpos = int((2*self.fen_width/(self.pos_reduc)/2))-14*len_name # calcul pour centrer le nom en fonction du nombre de lettre (c'est manuel mais.. pas d'autre methode)
        ypos = (int(self.fen_height/(self.pos_reduc))-20)/3
        self.window.blit(self.text_font_big.render(f"{nom_joueur}", True, color), (xpos,ypos)) #couleur à changer en fonction du joueur et de la couleur de son pays

        #choix nbr troupes
        text1 = "Combien de Troupes ?"
        text2 = "Combien de Dés pour attaquer ?"
        text3 = "Combien de Dés pour défendre ?"
        
        if self.view == 0: #renfo
            self.window.blit(self.text_font.render(f"Phase de renforcement", True, (255, 255, 255)),(int(0.625*self.fen_width), int(0.917*self.fen_height)))  
            #affichage nombre de troupes a repartir
            nbr_restant = self.a_qui_le_tour.troupe_a_repartir
            self.window.blit(self.text_font_big.render(str(nbr_restant), True, (255, 255, 255)), ((int((2*self.fen_width/(self.pos_reduc)-10)/2) - 30,int(self.fen_height/(self.pos_reduc))+75))) #RELATIF
        elif self.view == 1: #attaque
            self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (int(0.625*self.fen_width), int(0.917*self.fen_height)))
            self.window.blit(self.text_font.render(text1, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+(int(self.fen_height/(self.pos_reduc)-10))/2+20))
            self.window.blit(self.text_font.render(text2, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+120))
            self.window.blit(self.text_font.render(text3, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+190))
 
        elif self.view == 2: #deplacement
            self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (int(0.625*self.fen_width), int(0.917*self.fen_height)))
                    
        #Affiche les pays selectionnés et le joueur associé
        text4 = "Pays selectionnés :"
        self.window.blit(self.text_font.render(text4, True, (255, 255, 255)), (35,670)) #RELATIF
        select = self.select
        select_name = []
        select_player = []
        if select != []: #si un joueur selectionne un pays
            pos = [(35,710),(35,750),(250,710),(250,750)]  #RELATIF
            for country in select:
                select_name.append(country.nom_territoire)
                select_player.append(country.joueur.nom)
            for i in range(len(select)):
                self.window.blit(self.text_font.render(select_name[i]+", appartient à "+select_player[i], True, (255, 255, 255)), pos[i]) #place le nom du pays + propriétaire

        # Barre de texte
        self.barre_texte.afficher_texte()

        # Barre info
        self.barre_info.afficher_texte()


if __name__ == "__main__":
    import main
    menu = main.MainMenu()
    temp = menu.liste_joueurs
    out = []
    out.append(temp[0])
    out.append(temp[1])
    out.append(temp[4])
    

    window_pg = PygameWindow((menu.WIDTH, menu.HEIGHT), out)

    # run the main loop
    window_pg.main_loop()
    pygame.quit()
