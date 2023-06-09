# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 18:53:04 2023
@author: vince
"""
from random import randint, random, choice,shuffle
import time
import json
import csv
import pygame
import widgets
from math import inf


def des():
    x = randint(1, 6)
    return x

class territoire:
    def __init__(self, nom_zone, nom_territoire, mask, surface, joueur=None, nombre_troupes = 0,color=None):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone  # ce sera pour les bonus
        self.mask = mask
        self.surface = surface
        self.selec = 0
        self.collor = color


class Game:
    def __init__(self, liste_joueurs, fen_width, fen_height, barre_texte : widgets.BarreTexte):
        #initialisation des variables et chargement des données
        self.liste_joueurs = liste_joueurs #liste d'objet
        self.graphe = self.import_adjacence()
        self.dict_territoires = self.import_territoire()
        self.li_territoires = self.liste_territoires()
        self.liste_territoires_restant = self.li_territoires
        self.tps_debut = time.time()
        self.fen_width = fen_width
        self.fen_height = fen_height
        self.fac_reduc = 1.5 ###SETUP MANUEL POUR LA CARTE
        self.scores_attaquant = []
        self.scores_attaque = []
        # Closure pour print dans la barre
        self.print_barre = self.print_closure(barre_texte)



        #initialisation de la partie
        self.li_territoires_obj = self.init_territoires()
        self.placement_de_tous_les_joueurs()

        self.init_mission()
        self.nb_troupes_minimum = self.init_dict_nb_troupes_minimum()

    def init_dict_nb_troupes_minimum(self):
        nb_troupes_minimum=dict()
        for territoire in self.li_territoires:
            nb_troupes_minimum[territoire]=1
        return nb_troupes_minimum


    def print_closure(self, barre_texte : widgets.BarreTexte):
        """
        Fermeture permettant de remplacer la fonction `print` en envoyant l'output dans la barre
        """
        def message(string : str, err : bool = True):
            
            barre_texte.changer_texte([string], err=err, forceupdate=True)
        return message

    def droit_attaque(self, territoire_attaquant, territoire_attaque):
        """Cette fonction repère si l'attaque est autorisée ( vérification de l'adjacence des territoires, que le joueur
        ne s'attaque pas lui même et que le nombre de troupes sur le territoire attaquant soit suffisant)"""
        adjacence = self.verification_adjacence(territoire_attaquant,territoire_attaque)
        droit_attaque = False
        if territoire_attaquant.joueur != territoire_attaque.joueur : 
            if territoire_attaquant.nombre_troupes > 1 : 
                if adjacence == True : 
                    droit_attaque = True
                else : 
                    self.print_barre("Le territoire que vous voulez attaquer n'est pas adjacent à votre territoire attaquant", err=True)
            else : 
                self.print_barre("Vous n'avez pas assez de troupes pour attaquer ", err=True)
        else : 
            self.print_barre("Vous ne pouvez pas attaquer votre propre territoire !!", err=True)        
        
        return droit_attaque
    
    def choix_du_nombre_de_regiments_attaquant(self,territoire_qui_attaque,nombre_de_regiments_attaquant) :  
        """Cette fonction permet de vérifier que le nombre de troupes sélectionnées pour attaquer est cohérent avec le
        nombre de troupes du territoire"""
        test_nombre_de_regiments_attaquant = False
        if territoire_qui_attaque.nombre_troupes == 2 and nombre_de_regiments_attaquant==1:
            test_nombre_de_regiments_attaquant = True
        elif territoire_qui_attaque.nombre_troupes == 2 and nombre_de_regiments_attaquant!=1 : 
            self.print_barre("Vous ne pouvez utiliser qu'une seule troupe pour attaquer", err=True) 
        elif territoire_qui_attaque.nombre_troupes == 3  and (nombre_de_regiments_attaquant==1 or nombre_de_regiments_attaquant==2): 
            test_nombre_de_regiments_attaquant = True
        elif territoire_qui_attaque.nombre_troupes == 3  and (nombre_de_regiments_attaquant!=1 and nombre_de_regiments_attaquant!=2):
            self.print_barre("Vous devez choisir entre 1 et 2 régiments pour attaquer", err=True)
        elif territoire_qui_attaque.nombre_troupes > 3  and (nombre_de_regiments_attaquant==1 or nombre_de_regiments_attaquant==2 or nombre_de_regiments_attaquant==3): 
            test_nombre_de_regiments_attaquant = True
        elif territoire_qui_attaque.nombre_troupes > 3  and (nombre_de_regiments_attaquant!=1 and nombre_de_regiments_attaquant!=2 and nombre_de_regiments_attaquant!=3 ):
            self.print_barre("Vous devez choisir entre 1 et 2 et 3 régiments pour attaquer", err=True)

        return test_nombre_de_regiments_attaquant

    def nombre_de_des_a_jouer(self,territoire,nb_regiments_attaquant,nombre_de_des_joues, statut) : 
        """Cette fonction permet au joueur de vérifier que le nombre de dés est cohérent avec le nombre de troupes sélectionnées pour attaquer"""
        test_nombre_des = False
        if statut == "Attaquant" : 
            if nb_regiments_attaquant == 1 and nombre_de_des_joues == 1 : 
                test_nombre_des = True
            elif nb_regiments_attaquant == 1 and nombre_de_des_joues!=1 and territoire.nombre_troupes !=1 : 
                self.print_barre("Attaquant : Vous devez utiliser qu'un seul régiment pour attaquer avec ce nombre de troupes", err=True)
            elif nb_regiments_attaquant == 2 and (nombre_de_des_joues ==1 or nombre_de_des_joues ==2):
                test_nombre_des = True
            elif nb_regiments_attaquant == 2 and (nombre_de_des_joues !=1 and nombre_de_des_joues !=2):
                self.print_barre("Attaquant : Vous devez choisir parmi 1 ou 2 dés avec ce nombre de troupes! ", err=True)
            elif nb_regiments_attaquant == 3 and (nombre_de_des_joues ==1 or nombre_de_des_joues ==2 or nombre_de_des_joues ==3 ):
                test_nombre_des = True
        elif statut == "Attaqué" : 
            if (territoire.nombre_troupes == 1 or territoire.nombre_troupes == 2) and nombre_de_des_joues==1 :
                test_nombre_des = True
            elif (territoire.nombre_troupes == 1 or territoire.nombre_troupes == 2) and nombre_de_des_joues!=1 :
                self.print_barre("Attaqué : Vous devez jouer avec 1 dés au maximum", err=True)
            elif nombre_de_des_joues!=1 and nombre_de_des_joues!=2 : 
                self.print_barre("Attaqué: Vous devez choisir parmi 1 et 2 dés", err=True)
            elif territoire.nombre_troupes>=3 and (nombre_de_des_joues==1 or nombre_de_des_joues==2):
                test_nombre_des = True
        return test_nombre_des
    
    def attaque(self, territoire_attaquant, territoire_attaque,nombre_de_regiments_attaquant,nombre_de_des_attaquant,nombre_de_des_attaque):
        """"
        Fonction qui gère l'attaque d'un territoire par un joueur selon les règles du jeu RISK.
        https://www.regledujeu.fr/risk-regle-du-jeu/#des
        Le nombre de troupes perdues correspond au nombre de dés perdants. On classe les dés dans l'ordre décroissant 
        et on les compare 1 à 1. 
        """      
        territoire_conquis = False
        verif_des_attaquant = self.nombre_de_des_a_jouer(territoire_attaquant,nombre_de_regiments_attaquant,nombre_de_des_attaquant,"Attaquant")
        verif_des_defenseur = self.nombre_de_des_a_jouer(territoire_attaque,nombre_de_regiments_attaquant,nombre_de_des_attaque,"Attaqué")
        nb_regiments = self.choix_du_nombre_de_regiments_attaquant(territoire_attaquant,nombre_de_regiments_attaquant)
        droit_attaque = self.droit_attaque(territoire_attaquant, territoire_attaque)
        if droit_attaque and nb_regiments and verif_des_attaquant and verif_des_defenseur : 
                scores_attaquant = []
                scores_attaque = []
                gagnant = 0
                nb_des_a_comparer = 0 
                nb_des_attaquant  = nombre_de_des_attaquant
                nb_des_attaque = nombre_de_des_attaque
                nb_troupes_perdues_attaquant=0
                nb_troupes_perdues_attaque=0
                if nb_des_attaquant > nb_des_attaque : 
                    nb_des_a_comparer = nb_des_attaque
                else : 
                    nb_des_a_comparer = nb_des_attaquant
                for i in range(nb_des_attaquant):
                    scores_attaquant.append(des())
                for i in range(nb_des_attaque):
                    scores_attaque.append(des())
                scores_attaquant = tri_fusion(scores_attaquant)[::-1]
                scores_attaque = tri_fusion(scores_attaque)[::-1]
                self.scores_attaquant = scores_attaquant
                self.scores_attaque = scores_attaque
                i=0
                while i < nb_des_a_comparer and gagnant == 0:
                    if scores_attaquant[i] <= scores_attaque[i]:
                        territoire_attaquant.nombre_troupes -= 1
                        territoire_attaquant.joueur.nb_troupes-=1
                        nb_troupes_perdues_attaquant+=1   
                    if scores_attaquant[i] > scores_attaque[i]:
                        territoire_attaque.nombre_troupes -= 1
                        territoire_attaque.joueur.nb_troupes-=1
                        nb_troupes_perdues_attaque+=1
                    if territoire_attaque.nombre_troupes == 0:
                        territoire_attaque.joueur = territoire_attaquant.joueur
                        territoire_conquis = True 
                        gagnant = 1
                    i+=1
                self.print_barre(f" Le territoire attaquant a perdu {nb_troupes_perdues_attaquant} troupes,le territoire attaqué a perdu {nb_troupes_perdues_attaque} troupes")
        return territoire_conquis

    def import_territoire(self):
        with open('Fichiers/package.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues  # retourne un dictionnaire

    def liste_territoires(self):
        li = []
        for i in self.dict_territoires.values():
            for j in i:
                li.append(j)
        return li

    def transfert_troupes(self, territoire_de_depart, territoire_arrivee,nb_troupes_a_transferer):
        """
        Fonction qui gère le transfert de troupe d'un territoire à l'autre
        """
        transfert = False
        if self.verification_adjacence(territoire_de_depart, territoire_arrivee) == True:
            if nb_troupes_a_transferer <= 0:
                self.print_barre('Veuillez donner un nombre strictement positif de troupes à transférer')
            if nb_troupes_a_transferer < territoire_de_depart.nombre_troupes:
                territoire_de_depart.nombre_troupes = territoire_de_depart.nombre_troupes - nb_troupes_a_transferer
                territoire_arrivee.nombre_troupes += nb_troupes_a_transferer
                transfert = True
            else:
                self.print_barre('Vous ne pouvez pas transférer autant de troupes !!!!', err=True)  
        else:
            self.print_barre("Vos territoires ne sont pas adjacents, vous ne pouvez pas transférer des troupes, sélectionnez un autre territoire", err=True)
        
        return transfert
    
    def placement_de_tous_les_joueurs(self):
        """Cette fonction gère le placement des joueurs en début de partie en fonction du nombre de joueurs
        Elle fait appel aux fonctions joueurs au hasard et placement_initial pour cela. Elle attribue ainsi le nombre de 
        territoires nécessaires aux joueurs"""
        nb_joueurs = len(self.liste_joueurs)
        self.liste_territoires_restant = self.li_territoires_obj.copy()
        if nb_joueurs == 3:  
            for joueur in self.liste_joueurs:
                self.placement_initial(joueur, 35, 14)
        elif nb_joueurs == 4:
            joueurs_chanceux = self.joueur_au_hasard(self.liste_joueurs)    #on est obligé de faire ça car il y a 42 territoires et 42 n'est pas un multiple de 4
            for joueur in self.liste_joueurs:
                if self.liste_joueurs[joueurs_chanceux[0]] == joueur or self.liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 30, 11)
                else:
                    self.placement_initial(joueur, 30, 10)

        elif nb_joueurs == 5:
            joueurs_chanceux = self.joueur_au_hasard(self.liste_joueurs)  # idem que pour nombre de joueurs = 4 
            for joueur in self.liste_joueurs:
                if self.liste_joueurs[joueurs_chanceux[0]] == joueur or self.liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 25, 9)
                else:
                    self.placement_initial(joueur, 25, 8)
        else:
            for joueur in self.liste_joueurs:
                self.placement_initial(joueur, 20, 7)

    def joueur_au_hasard(self, liste_joueurs):
        """Permet de retourner 2 indices de joueurs dans la liste des joueurs : ils vont avoir un territoire en plus en début de partie"""
        liste_indice_joueurs_selectionnes = []
        indice_joueur_selectionne_1 = -1
        indice_joueur_selectionne_2 = -1
        while indice_joueur_selectionne_1 == indice_joueur_selectionne_2 or (indice_joueur_selectionne_1 == -1 or indice_joueur_selectionne_2==-1) :
            indice_joueur_selectionne_1 = randint(0, len(liste_joueurs) - 1)
            indice_joueur_selectionne_2 = randint(0, len(liste_joueurs) - 1)
        liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_1)
        liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_2)
        return liste_indice_joueurs_selectionnes

    def placement_initial(self, joueur, nb_troupes_a_placer, nb_territoire_a_occuper):
        """Gère le placment d'un joueur (il choisit où placer ses troupes en étant obligé d'avoir une troupe au minimum sur chaque
        territoire)"""
        joueur.nb_troupes = nb_troupes_a_placer  # depend du nombre de joueurs : l'info sera à mettre sur un fichier json que l'on lira
        i = 0
        territoires_occupés_par_le_joueur = []
        nombre_de_troupes_qu_il_reste_a_placer = nb_troupes_a_placer
        a=1
        fin = False
        while i < nb_territoire_a_occuper and fin == False:
            if len(territoires_occupés_par_le_joueur)<nb_territoire_a_occuper : 
                a = randint(0,(len(self.liste_territoires_restant))-1) 
                territoires_occupés_par_le_joueur.append(self.liste_territoires_restant[a])
                self.liste_territoires_restant.remove(self.liste_territoires_restant[a])
                if len(self.liste_territoires_restant)==0 : 
                    fin = True
            i += 1
        for territoire in territoires_occupés_par_le_joueur:
            territoire.nombre_troupes = 1  # On place une troupe par territoire
            territoire.joueur = joueur
            nombre_de_troupes_qu_il_reste_a_placer -= 1
            joueur.troupe_a_repartir = nombre_de_troupes_qu_il_reste_a_placer
    
    def import_adjacence(self):
        with open('Fichiers/adjacences_territoires.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            graphe = []
            for row in reader:
                graphe.append(row)
            return graphe


    def verification_adjacence(self, territoire1, territoire2):
        """
        Vérifie si deux territoires sont adjacents
        ⚠ l'indice dans la liste est pas le même que dans le graphe
        """
        graphe = self.graphe
        index1 = graphe[0].index(territoire1.nom_territoire)
        index2 = graphe[0].index(territoire2.nom_territoire)
        return graphe[index1][index2] == str(1)

    def init_territoires(self):
        """
        Initialise tout les objets territoires et renvoie la liste des territoires
        Il n'y a au début pas de joueur dessus, et 0 troupes, on les ajoutes après
        """
        li = []
        for area, countries_list in self.dict_territoires.items():
            for country in countries_list:
                image = pygame.image.load(f"Pictures/Maps/{country}.png").convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
                image = pygame.transform.scale(image, (int(self.fen_width/self.fac_reduc), int(self.fen_height/self.fac_reduc)))
                mask = pygame.mask.from_surface(image)
                li.append(territoire(area, country, mask, image))
        return li

    def check_continent_owner(self, continent: str, player):
        """Continent prend les valeurs Europe, Asie, Amérique du Nord, Amérique du Sud, Afrique, Océanie
        """
        own_continent = True 
        i =0 
        while i<(len(self.li_territoires_obj)) and own_continent == True : 
            if self.li_territoires_obj[i].nom_zone == continent and self.li_territoires_obj[i].joueur != player:
                own_continent = False
            i+=1
        return own_continent
    
    def liste_territoires_joueur(self, joueur):
            liste_territoires = []
            for i_territoire in self.li_territoires_obj:
                if i_territoire.joueur == joueur: #verifier si il faut verifier l'objet ou le nom
                    liste_territoires.append(i_territoire)
            return liste_territoires
    

    def count_player_territories(self, player):
        n_territoire = 0
        for i_territoire in self.li_territoires_obj:
            if i_territoire.joueur == player: #verifier si il faut verifier l'objet ou le nom
                n_territoire +=1
        return n_territoire

    def bonus(self, player):
        """
        Le bonus de troupe est octroyé à chaque tour à tout le monde, le nombre variant selon différent critère.
        Bonus pour le contrôle de territoire : 12-14 -> 1 régiment par territoire, 15-17 -> 2, 18-20 -> 3, 21-23 ->4,
        24-26 -> 5, 27-29 -> 6, 30-32 -> 7, 33-35 -> 8, 36-39-> 9, 40-42 -> 10
        Bonus pour le contrôle de continent : NA -> 5, SA -> 2, EU -> 5, AF -> 3, AS -> 7, OC -> 2
        """
        bonus = 0

        #bonus territoires
        n_territoire = self.count_player_territories(player)
        if 12 <= n_territoire <= 14:
            bonus+=1
        if 15 <= n_territoire <= 17:
            bonus+=2
        if 18 <= n_territoire <= 20:
            bonus+=3
        if 21 <= n_territoire <= 23:
            bonus+=4
        if 24 <= n_territoire <= 26:
            bonus+=5
        if 27 <= n_territoire <= 29:
            bonus+=6
        if 30 <= n_territoire <= 32:
            bonus+=7
        if 33 <= n_territoire <= 35:
            bonus+=8
        if 36 <= n_territoire <= 39:
            bonus+=9
        if 40 <= n_territoire <= 42:
            bonus+=10

        #bonus continent
        if self.check_continent_owner("Amérique du Nord", player):
            bonus+=5
        if self.check_continent_owner("Amérique du Sud", player):
            bonus+=2
        if self.check_continent_owner("Europe", player):
            bonus+=5
        if self.check_continent_owner("Afrique", player):
            bonus+=3
        if self.check_continent_owner("Asie", player): #Asinsa meilleur filière
            bonus+=7
        if self.check_continent_owner("Océanie", player):
            bonus+=2

        player.troupe_a_repartir += bonus

    def init_mission(self):
        for i in self.liste_joueurs:
            type_mission = randint(1, 8)
            if type_mission == 7:
                aim = choice(self.liste_joueurs)
                i.mission = Mission(type_mission, i.nom, self.li_territoires_obj, aim=aim.nom )
            else:
                i.mission = Mission(type_mission, i.nom, self.li_territoires_obj)

    def get_territoire_object(self,nom_territoire):
        territoire_obj=None
        for territoire in self.li_territoires_obj :
            if territoire.nom_territoire == nom_territoire : 
                territoire_obj=territoire
        return territoire_obj
    
    def get_player(self, str):
        for player in self.liste_joueurs:
            if (player.nom) == (str):
                return player
        return "Joueur non trouvé"

    
    def liste_voisin(self, territoire):
        """
        Fonction qui retourne la liste des territoires voisins d'un territoire donné
        """
        liste_voisin = []
        for i_territoire in self.li_territoires_obj:
            if self.verification_adjacence(territoire, i_territoire):
                liste_voisin.append(i_territoire)
        return liste_voisin

    def suggestion_trajet(self, territoire_depart, territoire_arrivee):
        """
        Fonction qui permet de suggérer le trajet le plus court entre deux territoires
        à l'aide de l'algorithme de Dijkstra
        on considère que le poids d'une arrête est le nombre de troupes présentes sur le territoire d'arrivée
        """

        #initialisation des variables
        candidats = self.li_territoires_obj.copy()

        graphe = {}
        for territoire in candidats:
            graphe[territoire] = {}
            for voisin in self.liste_voisin(territoire):
                graphe[territoire][voisin] = voisin.nombre_troupes if voisin.joueur != territoire_depart.joueur else 0

        chemins = {territoire_depart: (None, 0)} #pour un sommets, on a un tuple (prédesesseur, poids_total)
        parcourus = [territoire_depart]
        candidats.remove(territoire_depart)
        for sommet in candidats:
            chemins[sommet] = (None, inf)

        while parcourus[-1] != territoire_arrivee and candidats != []:
            #on actualise les poids pour chaque sommet
            """
            On parcours tout les sommets qui n'ont pas encore été visités
            On regarde si en passant par le dernier sommet visité, on a un poids plus faible
            Si oui, on actualise le poids du sommet, sinon, on garde la valeur précedente
            """
            for sommet in candidats:
                etape_precdente = parcourus[-1]
                #pb : pour le premier sommet, il faut prendre en compte qu'il n'y a pas de prédessesseur
                if sommet in graphe[etape_precdente]:
                    poids = chemins[etape_precdente][1] + graphe[etape_precdente][sommet] #poids du sommet = poids du sommet précédent + poids de l'arrête
                    if poids < chemins[sommet][1]:
                        chemins[sommet] = (etape_precdente, poids)

            #on récupère le sommet avec le poids le plus faible
            sommet_min = candidats[0]
            for c in candidats:
                if chemins[c][1] < chemins[sommet_min][1]:
                    sommet_min = c
                elif chemins[c][1] == chemins[sommet_min][1] and c == territoire_arrivee:
                    sommet_min = c

            candidats.remove(sommet_min)
            parcourus.append(sommet_min)

            #affichage (ces prints  reproduisent l'algorithme de Dijkstra fait à la main)

            """print('<départ>' if len(parcourus) == 0 else f"<{parcourus[-1].nom_territoire}({chemins[sommet_min][1]})>", end='/')
            for sommet in chemins.keys():
                print(f"{sommet.nom_territoire}({chemins[sommet][1]})" if sommet not in parcourus else "|||", end='/')
            print("\n")"""


        etapes = [territoire_arrivee]
        fin = False
        while not fin:
            etapes.append(chemins[etapes[-1]][0])
            if etapes[-1] == territoire_depart:
                fin = True
        return etapes[::-1]

def tri_fusion(liste):
    """Permet de retourner la liste de scores de dés dans l'ordre décroissant """
    liste_triee = []
    if len(liste) == 1:
        liste_triee = liste
    else:
        milieu = len(liste) // 2
        gauche = tri_fusion(liste[:milieu])
        droite = tri_fusion(liste[milieu:])
        liste_triee = fusion_triee(gauche, droite)
    return liste_triee


def fusion_triee(liste1, liste2):
    resultat = []
    i = j = 0
    while i < len(liste1) and j < len(liste2):
        if liste1[i] < liste2[j]:
            resultat.append(liste1[i])
            i += 1
        else:
            resultat.append(liste2[j])
            j += 1
    resultat.extend(liste1[i:] or liste2[j:])
    return resultat

class Mission:
    """
    Différent type de mission qu'un joueur peut être ammené à remplir, dans une variation des règle
    The missions are:
        capture Europe, Australia and one other continent #type = 1
        capture Europe, South America and one other continent #type = 2
        capture North America and Africa #type = 3
        capture Asia and South America #type = 4
        capture North America and Australia #type = 5
        capture 24 territories #type = 6
        destroy all armies of a named opponent or, in the case of being the named player oneself, to capture 24 territories # type = 7
        capture 18 territories and occupy each with two troops # type = 8
    """
    def __init__(self, type_mission:int, player:str, liste_territoire_obj,aim:str = None):
        self.type_mission = type_mission
        self.aim = aim #ne mettre une valeur que pour la mission 7, qui sera alors le joueur nommé
        self.player = player
        self.liste_territoire_obj = liste_territoire_obj #liste_territoire_obj est la liste de tout les objet territoire de associé à chacun des territoires de la carte
        self.detail = self.init_detail()

    def init_detail(self):
        if self.type_mission == 1:
            return "capture Europe, Australia and one other continent"
        elif self.type_mission == 2:
            return "capture Europe, South America and one other continent"
        elif self.type_mission == 3:
            return "capture North America and Africa"
        elif self.type_mission == 4:
            return "capture Asia and South America"
        elif self.type_mission == 5:
            return "capture North America and Australia"
        elif self.type_mission == 6:
            return "capture 24 territories"
        elif self.type_mission == 7:
            if self.aim == self.player:
                return "capture 24 territories"
            else:
                return f"destroy all armies of {self.aim}"
        elif self.type_mission == 8:
            return "capture 18 territories and occupy each with two troops"
    def check(self):
        #Pourquoi il y a pas de switch case en python putain
        if self.type_mission == 1:
            return self.check_mission1()
        elif self.type_mission == 2:
            return self.check_mission2()
        elif self.type_mission == 3:
            return self.check_mission3()
        elif self.type_mission == 4:
            return self.check_mission4()
        elif self.type_mission == 5:
            return self.check_mission5()
        elif self.type_mission == 6:
            return self.check_mission6()
        elif self.type_mission == 7:
            return self.check_mission7()
        elif self.type_mission == 8:
            return self.check_mission8()

    def check_continent_owner(self, continent:str):
        """Continent prend les valeurs Europe, Asie, Amérique du Nord, Amérique du Sud, Afrique, Océanie
        """
        own_continent = True
        i=0
        while i<len(self.liste_territoire_obj) and own_continent== True : 
            if self.liste_territoire_obj[i].nom_zone == continent and self.liste_territoire_obj[i].joueur.nom != self.player:
                own_continent = False
            i+=1
        return own_continent

    #perspective d'amélioration pour les check_mission : faire une fonction pour regrouper les missions similaires
    def check_mission1(self):
        """capture Europe, Australia and one other continent, return true si vérifié"""
        check = True
        others = 0
        if not (self.check_continent_owner("Europe") and self.check_continent_owner("Océanie")):
            check = False
            return check
        for continent in ["Asie", "Amérique du Nord", "Amérique du Sud", "Afrique"]:
            if self.check_continent_owner(continent):
                others+=1
        if others == 0:
            check = False
        return check

    def check_mission2(self):
        """capture Europe, South America and one other continent, return True si vérifié"""
        check = True
        others = 0
        if not (self.check_continent_owner("Europe") and self.check_continent_owner("Amérique du Sud")):
            check = False
            return check
        for continent in ["Asie", "Amérique du Nord", "Océanie", "Afrique"]:
            if self.check_continent_owner(continent):
                others += 1
        if others == 0:
            check = False
        return check

    def check_mission3(self):
        """capture North America and Africa"""
        check = True
        if not (self.check_continent_owner("Amérique du Nord") and self.check_continent_owner("Afrique")):
            check = False
        return check

    def check_mission4(self):
        """capture Asia and South America"""
        check = True
        if not (self.check_continent_owner("Asie") and self.check_continent_owner("Amérique du Sud")):
            check = False
        return check

    def check_mission5(self):
        """capture North America and Australia"""
        check = True
        if not (self.check_continent_owner("Amérique du Nord") and self.check_continent_owner("Océanie")):
            check = False
        return check

    def check_mission6(self):
        """capture 24 territories"""
        n = 0
        for i_territoire in self.liste_territoire_obj:
            if i_territoire.joueur.nom == self.player:
                n+=1
        return True if n >= 24 else False

    def check_mission7(self):
        """destroy all armies of a named opponent or,
        in the case of being the named player oneself, to capture 24 territories"""
        check = True
        if self.aim != self.player:
            for i_territoire in self.liste_territoire_obj:
                if i_territoire.joueur.nom == self.aim and i_territoire.nombre_troupes != 0:
                    check = False
            return check
        else:
            return self.check_mission6()

    def check_mission8(self):
        """capture 18 territories and occupy each with two troops
        J'ai un doute sur comment interpreter la mission mais je comprends qu'il faut controler
        18 territoires avec 2 troupes dessus, mais que si il y en a avec moins de troupes ils comptent
        juste pas
        """
        n = 0
        for i_territoire in self.liste_territoire_obj:
            if i_territoire.joueur.nom == self.player and i_territoire.nombre_troupes >= 2:
                n += 1
        return True if n >= 18 else False