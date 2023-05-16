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
        self.barre_texte = widgets.barreTexte(self.window, (0.333*self.fen_width, 0.837*self.fen_height), self.water.get_size()[0], 30)
        self.barre_texte.changer_texte("Bonjour ! Ceci est une barre de texte pour afficher des messages.")

        self.game = Rules.Game(self.liste_joueurs_obj, self.fen_width, self.fen_height, self.barre_texte)
        print(len(self.game.li_territoires_obj))
        print(type(self.liste_joueurs_obj))
        self.a_qui_le_tour = choice(self.liste_joueurs_obj) #celui qui commence
        self.text_font = pygame.font.Font("Fonts/ARLRDBD.TTF", 20)
        self.text_font_big = pygame.font.Font("Fonts/ARLRDBD.TTF", 50)
        self.select = []
        self.t = 0 #permet de revenir à la bonne vu après les missions
        self.deplacement = True
        self.placement_initial = []
        self.tour_initial = []

        #liste couleurs
        self.colors = [(0,255,0),(255,0,0),(0,0,255),(255,255,0),(255,0,255)]

        # Sélecteur de nombres
        self.init_couleurs()
        self.selnbr_troupes = widgets.selectNB((15, 300), 1, 1, 5) #max variable => à modifier
        self.selnbr_des = widgets.selectNB((15, 450), 1, 1, 3) #nombre de dés => affichage du bon nombre de dés en fonction de la selection



    def main_loop(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                #fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.closebutton_rect.collidepoint(pygame.mouse.get_pos()):
                    running = False

                #différentes vues
                elif self.view == 0: #renforcement
                    self.afficher_fenetre()
                    self.display_dice = False
                    self.window.blit(self.text_font.render(f"Phase de renforcement", True, (255, 255, 255)),(0.625*self.fen_width, 0.917*self.fen_height))

                    #affichage nombre de troupes a repartir
                    nbr_restant = self.a_qui_le_tour.troupe_a_repartir
                    self.window.blit(self.text_font_big.render(str(nbr_restant), True, (255, 255, 255)), ((int((2*self.fen_width/(self.pos_reduc)-10)/2) - 30,300)))
                    #affichage boutons + et - (juste pendant renforcement)
                    self.window.blit(self.plus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90,200))
                    self.window.blit(self.minus, (int((2*self.fen_width/(self.pos_reduc)-10)/2) +30 ,200))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #clic sur bouton +
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) - 90)), int(event.pos[1]-200)) #pour verifier si souris sur bouton sur le mask
                            if  self.plus_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour:
                                    if nbr_restant > 0:
                                        print("plus")
                                        self.select[0].nombre_troupes += 1 #ajout de la troupe sur le pays
                                        self.a_qui_le_tour.troupe_a_repartir -= 1 #retrait d'une troupe dans la liste des troupes a ajouter
                        except IndexError: None 
                        #clic sur bouton -
                        try:
                            scaled_pos = (int(event.pos[0]-(int((2*self.fen_width/(self.pos_reduc)-10)/2) +30)), int(event.pos[1]-200))
                            if  self.minus_mask.get_at(scaled_pos):
                                if self.select[0].joueur == self.a_qui_le_tour:
                                    if self.select[0].nombre_troupes > self.game.nb_troupes_minimum[self.select[0].nom_territoire]:
                                        print("moins")
                                        self.select[0].nombre_troupes -= 1
                                        self.a_qui_le_tour.troupe_a_repartir += 1
                        except IndexError: None 
                        
                       

                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
    
                            except IndexError:
                                pass
                              
                    if len(self.select) == 2 : 
                        self.changer_lumi(self.select[0])
                        self.select.remove(self.select[0])
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p and len(self.select) == 1:
                            self.game.ajout_de_troupes_sur_territoires(self.a_qui_le_tour, self.select[0], 1)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 0
                            self.view = 4
                        if event.key == pygame.K_RETURN :
                            print(self.placement_initial)
                            print(f"len(self.placement_initial) = {len(self.placement_initial)}")
                            print(f"len(self.liste_joueurs_obj) = {len(self.liste_joueurs_obj)}")
                            if self.a_qui_le_tour.troupe_a_repartir == 0:
                                self.changer_lumi(self.select[0])
                                self.select.remove(self.select[0])
                                if len(self.placement_initial) >= len(self.liste_joueurs_obj)-1:
                                    self.view = 1
                                else:
                                    self.placement_initial.append(self.a_qui_le_tour)
                                    self.next_player()
                            else:
                                print("Il vous reste encore des troupes à répartir")


                elif self.view == 1: #attaque
                    self.afficher_fenetre()
                    self.display_dice = True
                    self.window.blit(self.text_font.render(f"Phase d'attaque", True, (255, 255, 255)), (0.625*self.fen_width, 0.917*self.fen_height))
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        #selecteur nombre de regiment
                        #TODO changer l'ordre ou ça blit pour pas qu'il y a une sperposition bizzare
                        if self.selnbr_troupes(pygame.mouse.get_pos()) == 0:
                            self.selnbr_troupes.increment()
                        elif self.selnbr_troupes(pygame.mouse.get_pos()) == 1:
                            self.selnbr_troupes.decrement()
                        self.selnbr_troupes.draw(self.window)

                        #selecteur nombre de dés
                        if self.selnbr_des(pygame.mouse.get_pos()) == 0:
                            self.selnbr_des.increment()
                            shuffle(self.dice_list) #change les faces de dés affichées
                        elif self.selnbr_des(pygame.mouse.get_pos()) == 1:
                            self.selnbr_des.decrement()
                            shuffle(self.dice_list) #change les faces de dés affichées
                        self.selnbr_des.draw(self.window)

                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
                                    print(self.select)

                            except IndexError:
                                pass

                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            print("Vous ne pouvez pas attaquer avec un territoire qui ne vous appartient pas")
                            self.select=[]

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 1
                            self.view = 4
                        if event.type == 768 and len(self.select) == 2:
                            self.game.attaque(self.select[0], self.select[1])
                            print("attaque")
                        if event.key == pygame.K_RETURN:
                            self.view = 2
                            self.select=[]

                elif self.view == 2: #déplacement
                    self.afficher_fenetre()
                    self.display_dice = False
                    self.window.blit(self.text_font.render(f"Phase de déplacement", True, (255, 255, 255)), (0.625*self.fen_width, 0.917*self.fen_height))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for country in self.game.li_territoires_obj:
                            try:
                                scaled_pos = (int(event.pos[0]-2*int(self.fen_width/(self.pos_reduc))), int(event.pos[1]-int(self.fen_height/(self.pos_reduc))))
                                if country.mask.get_at(scaled_pos):
                                    print(f"{country.nom_territoire} : {pygame.mouse.get_pos()}") #pays sélectionné
                                    self.select_deux_surface(country)
                                    print(self.select)

                            except IndexError:
                                pass
                    if self.select != [] : 
                        if self.select[0].joueur != self.a_qui_le_tour :
                            print("Vous ne pouvez pas transférer des troupes depuis un territoire qui ne vous appartient pas")
                            self.select=[]
                        if len(self.select)==2 and self.select[1].joueur != self.a_qui_le_tour :
                            print("Vous ne pouvez pas transférer des troupes à un territoire qui ne vous appartient pas")
                            self.select=[]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.t = 2
                            self.view = 4
                        if event.key == pygame.K_t and len(self.select) == 2:
                            self.game.transfert_troupes(self.select[0], self.select[1],1)
                            self.deplacement = False
                        #reverifier si le déplacement est facultatif
                        if event.key == pygame.K_RETURN :
                            self.end_turn()

                elif self.view == 3: #win
                    self.afficher_fenetre()
                    self.display_dice = False
                    
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
        self.window.blit(self.water, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        self.window.blit(self.lines, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        self.window.blit(self.adios,(int(self.fen_width-self.adios.get_size()[0]-5),5))
        self.add_borders() #ajoute les bordures noires
        self.add_texts() #ajoute les texts
        if self.view == 1:
            self.selnbr_des.draw(self.window)   # Dessiner le sélecteur du nombre de dés
            self.selnbr_troupes.draw(self.window)   # Dessiner le sélecteur du nombre de troupes
            self.affiche_des(self.selnbr_des.etat) # met à jour les dés
        
        #territoires
        for country in self.game.li_territoires_obj:
            self.window.blit(country.surface, (2*int(self.fen_width/(self.pos_reduc)),int(self.fen_height/(self.pos_reduc))))
        #régiments
        for country in self.game.li_territoires_obj: #on est obligé de faire deux boucles pour que tout se superpose comme il faut
            self.window.blit(self.text_font.render(f"{country.nombre_troupes}", True, (0, 0, 0)),(self.coords[country.nom_territoire][0]*self.fen_width/(self.fac_reduc)+2*int(self.fen_width/(self.pos_reduc)), self.coords[country.nom_territoire][1]*self.fen_height/(self.fac_reduc)+int(self.fen_height/(self.pos_reduc))))#{country.nombre_troupes}
        
        # Barre de texte
        self.barre_texte.afficher_texte()



    def affiche_des(self, valeur):
        '''affiche le nombre de dés nécésaires selon le choix du joueur, affiche une valeur aléatoire'''
        if self.view == 1 :
            x = int((2*self.fen_width/(self.pos_reduc)-10)/2) - 150 #pour centrer les 3 dés
            pos = [(x,550),(x+120, 550),(x+240,550)] #écart de 120pixel entre les x (60 entre chaque dés)
            for i in range(valeur):
                self.window.blit(self.dice[self.dice_list[i]],pos[i]) #affiche une face du dé aléatoire



    def init_couleurs(self):
       '''
       initialise la couleur des territoires en début de partie
       avec les mask 
       '''
       for country in self.game.li_territoires_obj:
            surface = country.surface
            width, height = surface.get_size()
        
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
        print(r,g,b)
        if light == 0: #on veut assombrir l'image
            country.selec = 1
            
            r = int(r/1.5)
            g = int(g/1.5)
            b= int(b/1.5)
            print(r,g,b)
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
            select = []
            self.changer_lumi(country)
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
                self.game.nb_troupes_minimum[territoire]=self.game.li_territoires_obj[territoire].nombre_troupes
        self.select=[]

    def next_player(self):
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
        pygame.draw.rect(self.window, (0,0,0),(int(2*self.fen_width/(self.pos_reduc)),5,int(self.fen_width/(self.fac_reduc)-int(self.fen_height/(self.pos_reduc))),int(self.fen_height/(self.pos_reduc)-10)),4)
        #bordure adios
        self.closebutton_rect = pygame.draw.rect(self.window, (0,0,0),(int(self.fen_width-self.adios.get_size()[0]-5),5,self.adios.get_size()[0],self.adios.get_size()[1]),3)
        if self.view == 1:  #si phase attaque
            #bordure dés
            pygame.draw.rect (self.window, (0,0,0), (int((2*self.fen_width/(self.pos_reduc)-10)/2) - 180, 520, 360, 120),4)

    def add_texts(self):
        #TODO mettre les positions des textes en relatif
        '''ajoute tous les textes necessaires durant la partie'''
        #Nom du joueur en haut de la partie controle
        nom_joueur = self.a_qui_le_tour.nom #va chercher à qui le tour
        i = self.liste_joueurs_obj.index(self.a_qui_le_tour)
        color = self.colors[i] #recupere la couleur associée au joueur
        len_name = len(nom_joueur)
        xpos = int((2*self.fen_width/(self.pos_reduc)/2))-14*len_name # calcul pour centrer le nom en fonction du nombre de lettre (c'est manuel mais.. pas d'autre methode)
        self.window.blit(self.text_font_big.render(f"{nom_joueur}", True, color), (xpos,40)) #couleur à changer en fonction du joueur et de la couleur de son pays

        #choix nbr troupes
        text1 = "Combien de Troupes ?"
        text2 = "Combien de Dés ?"
        
        if self.view == 1:   
            self.window.blit(self.text_font.render(text1, True, (255, 255, 255)), (120,318))
            self.window.blit(self.text_font.render(text2, True, (255, 255, 255)), (120,468))

        #Affiche les pays selectionnés et le joueur associé
        text4 = "Pays selectionnés :"
        self.window.blit(self.text_font.render(text4, True, (255, 255, 255)), (35,670))
        select = self.select
        select_name = []
        select_player = []
        if select != []: #si un joueur selectionne un pays
            pos = [(35,710),(35,750),(250,710),(250,750)] 
            for country in select:
                select_name.append(country.nom_territoire)
                select_player.append(country.joueur.nom)
            for i in range(len(select)):
                self.window.blit(self.text_font.render(select_name[i]+", appartient à "+select_player[i], True, (255, 255, 255)), pos[i]) #place le nom du pays + propriétaire



if __name__ == "__main__":
    import main
    menu = main.MainMenu()
    temp = menu.liste_joueurs
    out = []
    out.append(temp[0])
    out.append(temp[1])
    out.append(temp[4])
    print(out)

    window_pg = PygameWindow((menu.WIDTH, menu.HEIGHT), out)

    # run the main loop
    window_pg.main_loop()
    pygame.quit()
