import pygame
from pygame.locals import *
from random import choice, shuffle
import json
import Rules
import widgets
import time
import subprocess
import csv
import sys
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
        self.dice_list1 = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5] #pour l'affichage random des dés, plusieurs fois 1-6 pour avoir plus de variété
        self.dice_list2 = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]

        # Barre de texte pour les messages
        self.barre_texte = widgets.BarreTexte(self.window, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.fac_reduc))+5), self.water.get_size()[0], 30, couleur_texte=(0,0,0), couleur_contour=(0,0,0))
        self.barre_texte.changer_texte([""])

        # Chronomètre
        self.chrono = widgets.Timer(self.window, (0.36*self.fen_width, int(self.fen_height-70)), couleur_texte=(0,0,0), taille_police=25)
        self.temps = time.time()

        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height, self.barre_texte)
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.text_font_big = pygame.font.Font("Fonts/ARLRDBD.TTF", 50)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions
        self.deplacement = True
        self.placement_initial = []
        self.tour_initial = []
        self.transfert_done = {}
        self.etat_mission = 0 #mission non affichée
        self.score = False #score du gagnant non mis à jour
        self.help_on = False #affichage aide OFF
        self.color_tempo = []
        self.end = False #partie fini True or false

        #liste couleurs
        self.colors = [(230 ,214,144),(132,92,2),(69,72,25),(144,117,2),(174,160,75),(114,125,0)]

        # Sélecteur de nombres
        self.init_couleurs()
        self.selnbr_troupes = widgets.SelectNB((15, int(self.fen_height/(self.pos_reduc))+(int(self.fen_height/(self.pos_reduc)-10))/2), 1, 1, 3)
        self.selnbr_des1 = widgets.SelectNB((15, int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)), 1, 1, 3) #nombre de dés => affichage du bon nombre de dés en fonction de la selection 
        self.selnbr_des2 = widgets.SelectNB((15, int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+140), 1, 1, 2) 

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
                        
                        if self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                            if self.etat_mission == 0:
                                self.t = 0
                                self.etat_mission = 1
                            elif self.etat_mission == 1:
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                                    self.view = self.t
                                    self.etat_mission = 0
                        #clic sur bouton +
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90)), int(event.pos[1]-int(self.fen_height/(self.pos_reduc)))) #pour verifier si souris sur bouton sur le mask
                            if  self.plus_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour:
                                    if nbr_restant > 0:           
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
                                    if self.select[0].nombre_troupes > self.game.nb_troupes_minimum[self.select[0].nom_territoire]:#cela permet de ne pas faire de transfert de troupes en retirant des troupes 
                                        self.select[0].nombre_troupes -= 1                                                         # à un territoire et en les ajoutant au compteur de troupes à répartir
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
                                    self.select_deux_surface(country)
    
                            except IndexError:
                                pass
                        

                        #clic sur next
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                        
                                #si toutes les troupes sont placées
                                if self.a_qui_le_tour.troupe_a_repartir == 0:
                                    try :
                                        self.changer_lumi(self.select[0])
                                        self.select.remove(self.select[0])
                                    except : pass
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
                    
                elif self.view == 1: #attaque
                    self.display_dice = True
                    self.afficher_fenetre()
                   
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                       
                       #selecteur nombre de regiment
                        if self.selnbr_troupes(pygame.mouse.get_pos()) == 0:
                            self.selnbr_troupes.increment()
                        elif self.selnbr_troupes(pygame.mouse.get_pos()) == 1:
                            self.selnbr_troupes.decrement()
                        self.selnbr_troupes.draw(self.window)

                        #selecteur nombre de dés 1 : attaque
                        if self.selnbr_des1(pygame.mouse.get_pos()) == 0:
                            self.selnbr_des1.increment()
                            shuffle(self.dice_list1) #change les faces de dés affichées
                        elif self.selnbr_des1(pygame.mouse.get_pos()) == 1:
                            self.selnbr_des1.decrement()
                            shuffle(self.dice_list1) #change les faces de dés affichées
                        self.selnbr_des1.draw(self.window)

                        #selecteur nombre de dés 2 : défence
                        if self.selnbr_des2(pygame.mouse.get_pos()) == 0:
                            self.selnbr_des2.increment()
                            shuffle(self.dice_list2) #change les faces de dés affichées
                        elif self.selnbr_des2(pygame.mouse.get_pos()) == 1:
                            self.selnbr_des2.decrement()
                            shuffle(self.dice_list2) #change les faces de dés affichées
                        self.selnbr_des2.draw(self.window)

                        #clic sur mission
                        if self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                            if self.etat_mission == 0:
                                self.t = 1
                                self.etat_mission = 1
                            elif self.etat_mission == 1:
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                                    self.view = self.t
                                    self.etat_mission = 0
                        
                        #check clic sur pays
                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos) and not self.help_on:
                                    self.select_deux_surface(country)
                            except IndexError:
                                pass
                        

                        #clic sur "Attaque"
                        try:
                            self.lancer_des = False
                            scaled_pos = (event.pos[0]-(self.fen_width-200),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                if len(self.select) == 2:
                                    if self.game.attaque(self.select[0], self.select[1], self.selnbr_troupes.etat, self.selnbr_des1.etat, self.selnbr_des2.etat):
                                        self.select[1].color = self.select[0].color
                                        self.select[1].joueur = self.select[0].joueur
                                        self.changer_couleur(self.select[1], self.select[1].color)
                                        troupe_attaque = self.selnbr_des1.etat
                                        self.barre_texte.changer_texte([f"Bravo {self.a_qui_le_tour.nom}, vous avez conquis {self.select[1].nom_territoire}"], err=True, forceupdate=True)
                                        self.view = 4 #REPARTITION TROUPES 
                                    
                        except IndexError : pass

                        #clic sur next, 
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                self.view = 2
                                self.barre_texte.changer_texte(["Fin de la phase d'attaque"], err=True, forceupdate=True)
                                self.empty_select()
                        except IndexError : pass

                        #clic sur help
                        try:
                            scaled_pos_help = (event.pos[0]-(self.fen_width-140),event.pos[1]-(self.fen_height-80))
                            if self.help.get_at(scaled_pos_help):
                                
                                if len(self.select) == 2 and self.select[1].joueur != self.a_qui_le_tour:
                                    if not self.help_on:
                                        nombre_pays = len(self.game.suggestion_trajet(self.select[0],self.select[1]))
                                        colors = self.generate_gradient(nombre_pays)
                                        for i in range(nombre_pays):
                                            country =  self.game.suggestion_trajet(self.select[0],self.select[1])[i]
                                            self.color_tempo.append(country.color)
                                            country.color = colors[i]
                                            self.changer_couleur(country,country.color)
                                            self.help_on = True
                                    elif self.help_on:
                                        for i in range(nombre_pays):
                                            self.game.suggestion_trajet(self.select[0],self.select[1])[i].color = self.color_tempo[i]
                                            self.changer_couleur(self.game.suggestion_trajet(self.select[0],self.select[1])[i],self.color_tempo[i])
                                        self.help_on = False
                                        self.color_tempo = []
                                else: self.barre_texte.changer_texte(["Vous n'avez pas besoin d'aide avec votre selection."], err=True, forceupdate=True)

                        except IndexError : pass
     


                        

                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            self.empty_select()
                            self.barre_texte.changer_texte(["Vous ne pouvez pas attaquer avec un territoire qui ne vous appartient pas"], err=True, forceupdate=True)

                elif self.view == 2: #déplacement OK FONCTIONNEL
                    self.afficher_fenetre()
                    self.display_dice = False
                    
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                        
                        #clic sur mission
                        if self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                            if self.etat_mission == 0:
                                self.t = 2
                                self.etat_mission = 1
                            elif self.etat_mission == 1:
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                                    self.view = self.t
                                    self.etat_mission = 0

                        #clic sur pays
                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    self.select_deux_surface(country)
                            except IndexError:
                                pass

                        #clic sur next, à voir si deplacement obligatoire
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                self.barre_texte.changer_texte(["Fin de la phase de déplacement"], err=True, forceupdate=True)
                                self.end_turn()
                                self.transfert_done = {}
                        except IndexError : pass

                        #clic sur transfert
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-150),event.pos[1]-(self.fen_height-80))
                            if self.transfert_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour and self.select[1].joueur == self.a_qui_le_tour :
                                    if len(self.select) == 2:
                                        if self.transfert_done == {}: #permet le premier transfert
                                            if self.game.transfert_troupes(self.select[0], self.select[1],1):
                                                self.transfert_done[(self.select[0], self.select[1])] = 1
                                                self.transfert_done[(self.select[1],self.select[0])] = -1


                                        elif (self.select[0],self.select[1]) in self.transfert_done.keys(): #si un transfert a deja été fait entre les deux pays : OK
                                            if self.game.transfert_troupes(self.select[0], self.select[1],1):    
                                                self.transfert_done[(self.select[0], self.select[1])] += 1
                                                self.transfert_done[(self.select[1],self.select[0])] -= 1

                                            if self.transfert_done[(self.select[0], self.select[1])] == 0: #si on est revenu à l'état initial > on enleve de la liste des transfert
                                                self.transfert_done.pop((self.select[0], self.select[1]))
                                            if self.transfert_done[(self.select[1], self.select[0])] == 0: #idem mais dans l'autre sens
                                                self.transfert_done.pop((self.select[1], self.select[0]))
                                        else:
                                            self.barre_texte.changer_texte(["Vous ne pouvez faire de deplacement qu'entre deux territoires"], err=True, forceupdate=True)
                                 
                                self.deplacement = False

                                    #VITTO VOIR POUR MESSAGE D'ERREUR SI NON ADJACENT
                        except IndexError : pass

                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            self.barre_texte.changer_texte(["Vous ne pouvez pas transférer des troupes depuis un territoire qui ne vous appartient pas"], err=True, forceupdate=True)
                            
                        if len(self.select)==2 and self.select[1].joueur != self.a_qui_le_tour :
                            self.barre_texte.changer_texte(["Vous ne pouvez pas transférer des troupes à un territoire qui ne vous appartient pas"], err=True, forceupdate=True)
                               
                elif self.view == 3: #win @CLEMENT A FINIR
                    self.afficher_fenetre()

                    self.window.blit(self.ecran_victoire, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
                    self.display_dice = False

                    #fin timer
                    if not self.end:
                        self.end = True

                    #ajouter +1 au score sur fichier csv joueurs pour le gagnat
                    if self.score == False:
                        self.joueur_win(self.a_qui_le_tour.nom)
                        self.score = True


                    

                elif self.view == 4: #repartition troupes apres victoire
                    self.display_dice = False
                    self.afficher_fenetre()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                        #clic sur mission
                        if self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                            self.t = 4
                            self.etat_mission
                        elif self.etat_mission == 1:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mission_rect.collidepoint(pygame.mouse.get_pos()):
                                self.view = self.t
                                self.etat_mission = 0

                        #clic sur bouton +
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90)), int(event.pos[1]-int(self.fen_height/(self.pos_reduc)))) #pour verifier si souris sur bouton sur le mask
                            if  self.plus_mask.get_at(scaled_pos):
                                
                                    if self.select[0].nombre_troupes > 1:        
                                        self.select[1].nombre_troupes += 1 #ajout de la troupe sur le pays
                                        self.select[0].nombre_troupes -= 1 
                                        
                                    else :  self.barre_texte.changer_texte([f"Nombre minimum de troupes atteint sur {self.select[0].nom_territoire}."], err=True, forceupdate=True)
                        except IndexError: pass

                        #clic sur bouton -
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) +30)), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                            if  self.minus_mask.get_at(scaled_pos):
                               
                                    if self.select[1].nombre_troupes > 1:
                                        self.select[1].nombre_troupes -= 1
                                        self.select[0].nombre_troupes += 1

                                    else :  self.barre_texte.changer_texte([f"Nombre minimum de troupes atteint sur {self.select[1].nom_territoire}."], err=True, forceupdate=True)
                        except IndexError: pass 

                     #clic sur next, 
                        try:
                            scaled_pos = (event.pos[0]-(self.fen_width-80),event.pos[1]-(self.fen_height-80))
                            if self.next_mask.get_at(scaled_pos):
                                if self.select[1].nombre_troupes >= troupe_attaque :
                                    self.view = 1 #retour à l'attaque
                                    self.barre_texte.changer_texte(["Fin de la phase de repartition"], err=True, forceupdate=True)
                                    self.changer_lumi(self.select[1])
                                    self.select = [self.select[0]]
                                elif self.select[1].nombre_troupes < troupe_attaque : 
                                    self.barre_texte.changer_texte([f"Vous devez ajouter au minimum {troupe_attaque} troupes sur le territoire conquis "], err=True, forceupdate=True) #force le joueur à ajouter au minimum le nombre de troupes avec lesquelles il a attaqué sur le territoire conquis.

                        except IndexError : pass

            self.framerate(1) # 1 fps minimum, j'espère que les pc vont tenir :))
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
            dice = pygame.transform.scale(dice, (40,40))
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
        #bouton mission
        self.mission = pygame.image.load("Pictures/mission.png").convert_alpha()
        self.mission = pygame.transform.scale(self.mission,((self.adios.get_size()[1]-20)*1.93,self.adios.get_size()[1]-20))
        #bouton aide (affichage chemin plus efficace )
        self.help = pygame.image.load("Pictures/help.png").convert_alpha()
        self.help = pygame.transform.scale(self.help,(50,50))
        self.help_mask = pygame.mask.from_surface(self.help)

    def charger_coord_texte(self):
        with open('Fichiers/coords.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues

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

    def generate_gradient(self, x):
        gradient = []
        step = 180 // (x-1)  # calcul l'interval par couleur
    
        for i in range(x):
            value = 200 - (step * i)   # diminue l'intensité à chaque tour, minimum 
            color= (value,value,value)
            gradient.append(color) 
    
        return gradient
    
    def afficher_fenetre(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """

        #bg
        self.window.blit(self.bg,(0,0))
        #
        if self.view != 3: #pas de carte pour les fenetres win 
            self.window.blit(self.water, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
            self.window.blit(self.lines, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        #bouton quitter
        self.window.blit(self.adios,(int(self.fen_width-self.adios.get_size()[0]-5),5))
        #bouton next
        self.window.blit(self.next,(int(self.fen_width-80),int(self.fen_height-80)))
        # bouton mission top_secret
        if self.etat_mission == 0: 
            self.window.blit(self.mission,(2*int(self.fen_width/(self.pos_reduc))+(int(self.fen_width/(self.fac_reduc)-5)-self.adios.get_size()[0]-5)/2-((self.adios.get_size()[1]-50)*1.93)/2,15))
        self.add_borders() #ajoute les bordures noires
        self.add_texts() #ajoute les texts
        if self.view == 0 or self.view == 4 : #renforcement ou repartition
            #affichage boutons + et - (juste pendant renforcement)
            self.window.blit(self.plus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90,int(self.fen_height/(self.pos_reduc))))
            self.window.blit(self.minus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) +30 ,int(self.fen_height/(self.pos_reduc))))
        elif self.view == 1: #attaque
            self.selnbr_des1.draw(self.window)   # Dessiner le sélecteur du nombre de dés d'attaque
            self.selnbr_des2.draw(self.window)   # Dessiner le sélecteur du nombre de dés de defence
            self.selnbr_troupes.draw(self.window)   # Dessiner le sélecteur du nombre de troupes
            self.affiche_des(self.selnbr_des1.etat, 1) # met à jour les dés
            self.affiche_des(self.selnbr_des2.etat , 2)
            #bouton aide
            self.window.blit(self.help,(int(self.fen_width-140),int(self.fen_height-80)))
            #affichage icone attaque
            self.window.blit(self.attack,(int(self.fen_width)-200,int(self.fen_height-80)))

        elif self.view == 2: #deplacement
            self.window.blit(self.transfert,(int(self.fen_width-150),int(self.fen_height-80)))
        elif self.view == 3: #win
            self.window.blit(self.ecran_victoire, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        if self.view != 3:  # pas de carte pour les fenetres win et mission
            #territoires
            for country in self.game.li_territoires_obj:
                self.window.blit(country.surface, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
            #régiments
            for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
                self.window.blit(self.text_font.render(f"{country.nombre_troupes}", True, (0, 0, 0)),(self.coords[country.nom_territoire][0]*self.fen_width/(self.fac_reduc)+2*int(self.fen_width/(self.pos_reduc)), self.coords[country.nom_territoire][1]*self.fen_height/(self.fac_reduc)+int(self.fen_height/(self.pos_reduc))))#{country.nombre_troupes}
        
        # Chrono   
        if not self.end :    
            self.chrono.update()

    def framerate(self, temps : float):
        """
        Si le temps depuis le dernier rafraîchissement est plus que `temps`, ça rafraîchit.
        (Sert à forcer le rafraîchissement du chronomètre. En fin de compte on aura que le jeu
        se rafraîchit au moins une fois toutes les secondes, mais plus si nécessaire)


        N.B. : On ne force pas le rafraîchissement, vu que la fonction est appellée juste avant de le faire de toute façon.
        Ça ferait double-emploi.

        """
        if (time.time() - self.temps) >= temps:
            self.afficher_fenetre()

    def affiche_des(self, valeur, etat): #ATTAQUE
        '''affiche le nombre de dés nécésaires selon le choix du joueur, affiche une valeur aléatoire'''
        if self.view == 1 :
            if etat == 1 : #des attaque
                x = int((2*self.fen_width/(self.pos_reduc)-10)/2) - 100 #pour centrer les 3 dés
                y = int(0.234*self.fen_width)
                pos = [(x,y),(x+80, y),(x+160,y)] #écart de 90pixel entre les x (60 entre chaque dés) 
                for i in range(valeur): 
                    if len(self.game.scores_attaquant)== valeur : 
                        self.window.blit(self.dice[self.game.scores_attaquant[i]- 1],pos[i])   #permet d'afficher les valeurs des dés tirés durant l'attaque
                    else  : 
                        self.window.blit(self.dice[self.dice_list1[i]],pos[i]) #affiche une face du dé aléatoire
            if etat == 2: #des defence
                x = int((2*self.fen_width/(self.pos_reduc)-10)/2) - 60 #pour centrer les 3 dés
                y = int(0.319*self.fen_width)
                pos = [(x,y),(x+80, y)] #écart de 120pixel entre les x (60 entre chaque dés) 
                for i in range(valeur):
                    if len (self.game.scores_attaque) == valeur :     
                        self.window.blit(self.dice[self.game.scores_attaque[i]- 1],pos[i])  #permet d'afficher les valeurs des dés tirés durant l'attaque
                    else : 
                        self.window.blit(self.dice[self.dice_list2[i]],pos[i]) #affiche une face du dé aléatoire

    def add_borders(self):
        #bordure autour de la map
        pygame.draw.rect(self.window, (0,0,0), (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc)),int(self.fen_width/(self.fac_reduc)-5),int(self.fen_height/(self.fac_reduc))),3)
        #bordure controles
        pygame.draw.rect(self.window, (0,0,0),(5,5, int(2*self.fen_width/(self.pos_reduc)-10),int(self.fen_height - 10)),4)
        #bordure box mission
        self.mission_rect = pygame.draw.rect(self.window, (0,0,0),(2*int(self.fen_width/(self.pos_reduc)),5, int(self.fen_width/(self.fac_reduc)-5)-self.adios.get_size()[0]-5,self.adios.get_size()[1]),4)
        #bordure adios
        self.closebutton_rect = pygame.draw.rect(self.window, (0,0,0),(int(self.fen_width-self.adios.get_size()[0]-5),5,self.adios.get_size()[0],self.adios.get_size()[1]),3)
        
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
            self.window.blit(self.text_font_big.render(str(nbr_restant), True, (255, 255, 255)), ((int((2*self.fen_width/(self.pos_reduc)-10)/2) - 30,int(self.fen_height/(self.pos_reduc))+75)))
        elif self.view == 1: #attaque
            self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (int(0.625*self.fen_width), int(0.917*self.fen_height)))
            self.window.blit(self.text_font.render(text1, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+(int(self.fen_height/(self.pos_reduc)-10))/2+20))
            self.window.blit(self.text_font.render(text2, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+20))
            self.window.blit(self.text_font.render(text3, True, (255, 255, 255)), (120,int(self.fen_height/(self.pos_reduc))+int(self.fen_height/(self.pos_reduc)-10)+160))
 
        elif self.view == 2: #deplacement
            self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (int(0.625*self.fen_width), int(0.917*self.fen_height)))
        if self.etat_mission == 1:
            self.window.blit(self.text_font.render(f"Mission", True, (255, 255, 255)),(2*int(self.fen_width/(self.pos_reduc))+(int(self.fen_width/(self.fac_reduc)-5)-self.adios.get_size()[0]-5)/2-37, 0.0405*self.fen_height)) 
            x = len(self.a_qui_le_tour.mission.detail) #pour centrer plus facilement dans la barre
            self.window.blit(self.text_font.render(f"{self.a_qui_le_tour.mission.detail}", True, (0, 0, 0)),(2*int(self.fen_width/(self.pos_reduc))+(int(self.fen_width/(self.fac_reduc)-5)-self.adios.get_size()[0]-5)/2-((10*x)/2), 0.069*self.fen_height)) 
        #Affiche les pays selectionnés et le joueur associé
        text4 = "Pays selectionnés :"
        self.window.blit(self.text_font.render(text4, True, (255, 255, 255)), (int(0.023*self.fen_width),int(0.694*self.fen_height))) #RELATIF
        select = self.select
        select_name = []
        select_player = []
        if select != []: #si un joueur selectionne un pays
            x = int(0.023*self.fen_width)
            y = int(0.694*self.fen_height)
            pos = [(x,y+40),(x,y+120),(x,y+80),(x,y+160)]  #RELATIF
            for country in select:
                select_name.append(country.nom_territoire)
                select_player.append(country.joueur.nom)
            for i in range(len(select)):
                self.window.blit(self.text_font.render(select_name[i], True, (255, 255, 255)), pos[i]) #place le nom du pays + propriétaire
                self.window.blit(self.text_font.render("appartient à "+select_player[i], True, (255, 255, 255)), pos[i+2])
        if not self.end:
            self.heures = self.chrono.heures
            self.minutes = self.chrono.minutes
            self.secondes = self.chrono.secondes
        if self.end:
            self.window.blit(self.text_font.render(f"Partie terminée, {self.a_qui_le_tour} a gagné ! Elle a duré {self.heures}h {self.minutes}min {self.secondes}s ", True, (0,0,0)), (0.36*self.fen_width, int(self.fen_height-70)))




        # Barre de texte
        self.barre_texte.afficher_texte()

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
        country.surface = new_surface

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
        elif len(select) == 2 and country == select[1]:
            select = select [:-1]
            self.changer_lumi(country)
        elif len(select)==1 and country == select[0]:
            self.changer_lumi(country)
            select = []
        self.select = select

    def empty_select(self):
        """vide self.select et deselectionne les pays"""
        for country in self.select:
            self.changer_lumi(country)
        self.select = []

    def end_turn(self):
        """
        On vérifie si le joueur a gagné, si oui, on affiche la victoire, sinon on passe au joueur suivant
        """
        self.game.bonus(self.a_qui_le_tour)
        if len(self.tour_initial) <= 3:
            self.tour_initial.append(self.a_qui_le_tour)
        if self.a_qui_le_tour.mission.check() :
            self.view = 3
        else:
            self.next_player()
            self.deplacement = True
            self.view = 0 if self.a_qui_le_tour in self.tour_initial else 1
        if self.view == 0 : 
            for territoire in self.game.li_territoires: 
                self.game.nb_troupes_minimum[territoire]=self.game.get_territoire_object(territoire).nombre_troupes
        self.empty_select()

    def next_player(self):
        '''passe au joueur suivant dans la partie'''
        self.check_loss()

        if self.liste_joueurs_obj[-1] == self.a_qui_le_tour:
            self.a_qui_le_tour = self.liste_joueurs_obj[0]
        else:
            self.a_qui_le_tour = self.liste_joueurs_obj[self.liste_joueurs_obj.index(self.a_qui_le_tour) + 1]

    def check_loss(self):
        '''verifie si un joueur a perdu tout ses territoires et le retire de la liste de joueurs'''
        for player in self.liste_joueurs_obj:
            list_play= []
            for country in self.game.li_territoires_obj:
                if country.joueur == player:
                    list_play.append(country)
            if list_play == []:
                self.liste_joueurs_obj.remove(player)

    def afficher_mission(self):
        if self.etat_mission == 0:
            self.etat_mission = 1
        elif self.etat_mission == 1:
            self.etat_mission = 0

    def joueur_win(self, joueur:str):
        '''met à jour le score du gagnant'''
        csv_file = "Fichiers/Joueurs.csv"
        # Ouvre le fichier CSV en mode lecture
        with open(csv_file, 'r') as file:
            # Lire les données CSV
            reader = csv.reader(file)
            rows = list(reader)

        # Parcourir chaque ligne du CSV
        indice_row = 0
        arret = False
        while indice_row < len(rows) and arret == False : 
            if rows[indice_row][0] == joueur :
                # on incremente en faisant attention aux types de variables
                rows[indice_row][2] = str(int(rows[indice_row][2]) + 1)
                arret = True # On sort de la boucle quand on a trouvé le nom pour limiter la complexité
            indice_row+=1

        # Écrire les données mises à jour dans le fichier CSV
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        

if __name__ == "__main__": #pour debug
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
