# -*- coding: utf-8 -*-
"""

Created on Tue Mar 28 18:53:04 2023

@author: vince
"""
from random import randint, random, choice
import time
import json
import csv
import pygame


def des():
    x = randint(1, 6)
    return x
#Fais une fonction qui renvoie des chiffres au hasard pour imiter le comportement d'un dés

class Timer:

    def __init__(self, duree):
        self.reference = time.time()
        self.duree = duree

    def temps_restant(self):
        return self.reference - (time.time() - self.reference)


class troupes:
    def __init__(self, nom, type, joueur, territoire):
        self.nom = nom
        self.type = type
        self.joueur = joueur
        self.territoire = territoire


class territoire:
    def __init__(self, nom_zone, nom_territoire, mask, surface, joueur=None, nombre_troupes = 0):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone  # ce sera pour les bonus
        self.mask = mask
        self.surface = surface

class Player: #voir avec antoine si on peut pas utiliser directement sa classe Joueur
    def __init__(self, nom):
        self.nom = nom

class Game:
    def __init__(self, liste_joueurs, fen_width, fen_height):
        #initialisation des variables et chargement des données
        self.liste_joueurs = liste_joueurs #liste d'objet
        self.graphe = self.import_adjacence()
        self.dict_territoires = self.import_territoire()
        self.li_territoires = self.liste_territoires()
        self.liste_territoires_restant = self.li_territoires
        self.tps_debut = time.time()
        self.fen_width = fen_width
        self.fen_height = fen_height


        #initialisation de la partie
        self.li_territoires_obj = self.init_territoires()
        self.placement_de_tous_les_joueurs()
        self.init_mission()



    def droit_attaque(self, territoire_attaquant, territoire_attaque):
        """Cette fonction repère si l'attaque est autorisée"""
        adjacence = self.verification_adjacence(territoire_attaquant,territoire_attaque)
        proprietaires_differents = False
        troupes_suffisantes = False
        droit_attaque = False
        if territoire_attaquant.joueur != territoire_attaque.joueur : 
            proprietaires_differents = True
            if territoire_attaquant.nombre_troupes > 1 : 
                troupes_suffisantes = True
                if adjacence == True : 
                    droit_attaque = True
                else : 
                    print("Le territoire que vous voulez attaquer n'est pas adjacents à votre territoire attaquant")
            else : 
                print ("Vous n'avez pas assez de troupes pour attaquer")
        else : 
            print("Vous ne pouvez pas attaquer votre propre territoire !!")        
        
        return droit_attaque
    
    def choix_du_nombre_de_regiments_attaquant(self,territoire_qui_attaque) :  
        """Cette fonction permet de définir combien de régiments attaquent"""
        nombre_de_regiments_attaquant = 0
        choix = 0
        while nombre_de_regiments_attaquant == 0 : 
            if territoire_qui_attaque.nombre_troupes == 2 :
                nombre_de_regiments_attaquant = 1
            if territoire_qui_attaque.nombre_troupes == 3 : 
                choix = int(input('Voulez-vous attaquer avec 1 ou 2 regiments'))
                if choix != 2 and choix != 1 : 
                    print ('Choisissez un nombre de régiments attaquant parmi 2 et 3')
                else : 
                    nombre_de_regiments_attaquant = choix
            if territoire_qui_attaque.nombre_troupes > 3 : 
                choix = int(input('Voulez-vous attaquer avec 1,2 ou 3 regiments'))
                if choix != 1 and choix != 2 and choix !=3 : 
                    print ('Choisissez un nombre de régiments attaquant parmi 1, 2 et 3')
                else : 
                    nombre_de_regiments_attaquant = choix

        return nombre_de_regiments_attaquant

    def nombre_de_des_a_jouer(self,territoire,statut) : 
        """Cette fonction permet au joueur de déterminer avec combien de dés il veut jouer. Evidemment il a intérêt a jouer avec le plus de dés possibles
        mais il peut faire un autre choix ..."""
        nombre_de_des_a_jouer = 0
        nb_regiments_attaquant = 0
        if statut == "Attaquant" : 
            while nombre_de_des_a_jouer == 0 : 
                nb_regiments_attaquant = self.choix_du_nombre_de_regiments_attaquant(territoire)    
                if nb_regiments_attaquant == 1 : 
                    nombre_de_des_a_jouer =  1 
                if nb_regiments_attaquant == 2 :
                    choix = int(input("Vous pouvez utiliser 1 ou 2 dés. Combien en voulez vous ? "))
                    if choix != 1 and choix != 2 :
                        print("Vous devez choisir parmi 1 et 2 dés")
                    else : 
                        nombre_de_des_a_jouer = choix
                if nb_regiments_attaquant == 3 :
                    choix = int(input("Vous pouvez utiliser 1 ou 2 ou 3 dés. Combien en voulez vous ? "))
                    if choix != 1 and choix != 2 and choix != 3 :
                        print("Vous devez choisir parmi 1, 2 et 3 dés")
                    else : 
                        nombre_de_des_a_jouer = choix
        elif statut == "Attaqué" : 
            while nombre_de_des_a_jouer == 0 : 
                if territoire.nombre_troupes == 1 or territoire.nombre_troupe == 2 :
                    nombre_de_des_a_jouer = 1
                else : 
                    choix = int(input("Vous pouvez utiliser 1 ou 2 dés pour vous défendre. Que choisissez vous ? "))
                    if choix != 1 and choix != 2 :
                        print("Vous devez choisir parmi 1 et 2 dés")
                    else : 
                        nombre_de_des_a_jouer = choix
        return nombre_de_des_a_jouer, nb_regiments_attaquant
    
    def attaque(self, territoire_attaquant, territoire_attaque):
        """"
        Fonction qui gère l'attaque d'un territoire par un joueur
        territoire_attaquant et territoire_attaque sont des objets
        LE NOMBRE DE DES LANCES PAR L ATTAQUANT EST SEULEMENT DE 3 S IL A 4
        REGIMENT OU PLUS ET QU IL CHOISIT D ATTAQUER AVEC 3 REGIMENTS 
        LE NOMBRE DE DES LANCES PAR CELUI QUI ATTAQUE EST SEULEMENT DE 2 AU MAXIMUM SI IL A 3 REGIMENTS OU PLUS SUR LE TERRITOIRE

        LE NOMBRE DE DES LANCES EST CHOISI PAR LE JOUEUR 
        
        https://www.regledujeu.fr/risk-regle-du-jeu/#des
        """      
        self.droit_attaque(territoire_attaquant, territoire_attaque)
        if self.droit_attaque(territoire_attaquant, territoire_attaque) == True : 
                scores_attaquant = []
                scores_attaque = []
                gagnant = 0
                nb_des_a_comparer = 0 
                nb_des_attaquant, nb_regiments_attaquant  = self.nombre_de_des_a_jouer(territoire_attaquant,"Attaquant")
                nb_des_attaque = self.nombre_de_des_a_jouer(territoire_attaque,"Attaqué")[0]
                if nb_des_attaquant > nb_des_attaque : 
                    nb_des_a_comparer = nb_des_attaque
                else : 
                    nb_des_a_comparer = nb_des_attaquant
                for i in range(nb_des_attaquant):
                    scores_attaquant.append(des())
                for i in range(nb_des_attaque):
                    scores_attaque.append(des())
                scores_attaquant = tri_fusion(scores_attaquant)
                scores_attaque = tri_fusion(scores_attaque)
                i=0
                while i < nb_des_a_comparer and gagnant == 0:
                    if scores_attaquant[i] <= scores_attaque[i]:
                        territoire_attaquant.nombre_troupes -= 1
                        territoire_attaquant.joueur.nb_troupes-=1    
                        print("Le territoire attaquant perd une troupe")
                        i += 1
                    if scores_attaquant[i] > scores_attaque[i]:
                        territoire_attaque.nombre_troupes -= 1
                        territoire_attaque.joueur.nb_troupes-=1
                        print("Le territoire attaqué perd une troupe")
                        i += 1
                    if territoire_attaque.nombre_troupes == 0:
                        territoire_attaquant.joueur.territoires.apppend(territoire_attaque)
                        territoire_attaque.joueur.territoires.remove(territoire_attaque)
                        territoire_attaque.joueur = territoire_attaquant.joueur
                        self.changer_couleur(territoire_attaque)
                        print('Attaquant, vous avez gagné un nouveau territoire, déplacez vos troupes pour l occuper')
                        nombre_de_troupes_a_transferer = 0 
                        while nombre_de_troupes_a_transferer < nb_regiments_attaquant or nombre_de_troupes_a_transferer > territoire_attaquant.nombre_troupes :
                            nombre_de_troupes_a_transferer = input("Les troupes attaquante doivent occuper ce territoire, le temps que d'autres renforts arrivent. Combien voulez vous en laisser ( il faut au minimum que vous utilisiez les régiments qui attaquaient? ")
                        self.transfert_troupes(territoire_attaquant, territoire_attaque, nombre_de_troupes_a_transferer)
                        gagnant = 1
        else : 
            print("Vous ne pouvez pas attaquer")

    def import_territoire(self):
        with open('Fichiers/package.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues  # retourne un dictionnaire

    def liste_territoires(self):
        li = []
        for i in self.import_territoire().values():
            li.append(i)
        return li

    def transfert_troupes(self, territoire_de_depart, territoire_arrivee):
        """
        Fonction qui gère le transfère de troupe d'un territoire à l'autre
        """
        if self.verification_adjacence(territoire_de_depart, territoire_arrivee) == True:
            nb_troupes_a_transferer = int(input("Nombre de troupes à transférer ?"))
            if nb_troupes_a_transferer <= 0:
                print('Veuillez donner un nombre strictement positif de troupes à transférer')
            if nb_troupes_a_transferer < territoire_de_depart.nombre_troupes:
                territoire_de_depart.nombre_troupes = territoire_de_depart.nombre_troupes - nb_troupes_a_transferer
                territoire_arrivee.nombre_troupes += nb_troupes_a_transferer
            else:
                print('Vous ne pouvez pas transférer autant de troupes !!!!')  # il faut rajouter la condition de proximité avec la matrice d'adjacence
        else:
            print("Vos territoires ne sont pas adjacents, vous ne pouvez pas transférer des troupes, sélectionnez un autre territoire")



    def placement_de_tous_les_joueurs(self):
        """Cette fonction gère le placement des joueurs en début de partie en fonction du nombre de joueurs
        Elle fait appel aux fonctions joueurs au hasard et placement_initial pour cela"""
        nb_joueurs = len(self.liste_joueurs)
        self.liste_territoires_restant = self.li_territoires_obj.copy()
        if nb_joueurs == 2:
            for joueur in self.liste_joueurs:
                self.placement_initial(joueur, 40, 14)  # il faut ajouter l'armée neutre qui a le meme nombre de territoires
        elif nb_joueurs == 3:  # et 2 régiments par territoire
            for joueur in self.liste_joueurs:
                self.placement_initial(joueur, 35, 14)
        elif nb_joueurs == 4:
            joueurs_chanceux = self.joueur_au_hasard(self.liste_joueurs)
            for joueur in self.liste_joueurs:
                if self.liste_joueurs[joueurs_chanceux[0]] == joueur or self.liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 30, 11, self.liste_territoires_restant)
                else:
                    self.placement_initial(joueur, 30, 10)

        elif nb_joueurs == 5:
            joueurs_chanceux = self.joueur_au_hasard(self.liste_joueurs)
            for joueur in self.liste_joueurs:
                if self.liste_joueurs[joueurs_chanceux[0]] == joueur or self.liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 25, 9)
                else:
                    self.placement_initial(joueur, 25, 8)
        else:
            for joueur in self.liste_joueurs:
                self.placement_initial(joueur, 20, 7)

    def joueur_au_hasard(self, liste_joueurs):
        """Permet de retourner 2 indices de joueurs dans la liste des joueurs qui vont avoir un territoire en plus en début de partie"""
        liste_indice_joueurs_selectionnes = []
        indice_joueur_selectionne_1 = -1
        indice_joueur_selectionne_2 = -1
        while indice_joueur_selectionne_1 == indice_joueur_selectionne_2:
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
            print(territoire.nom_territoire)
            self.changer_couleur(territoire)
        
        #while nombre_de_troupes_qu_il_reste_a_placer > 0:
            #nombre_de_troupes_qu_il_reste_a_placer = self.ajout_de_troupes_sur_territoires(joueur)
            

        # il faut que le joueur tire des territoires au hasard où il placera ses troupes comme il le souhaite avec toujours au minimum une troupe sur chaque territoire occupé
    def ajout_de_troupes_sur_territoires(self, joueur, territoire, nombre):
        nombre_de_troupes_qu_il_reste_a_placer = joueur.troupe_a_repartir
        liste_territoires_joueurs = self.liste_territoires_joueur(joueur)
        if nombre > nombre_de_troupes_qu_il_reste_a_placer:  # Le joueur ajoute des troupes sur les territoires qu'il
            print("Il ne vous reste pas assez de troupes !!")
        else:
            territoire.nombre_troupes += nombre
            nombre_de_troupes_qu_il_reste_a_placer -= nombre
        joueur.troupe_a_repartir = nombre_de_troupes_qu_il_reste_a_placer
        return nombre_de_troupes_qu_il_reste_a_placer 
    
    def import_adjacence(self):
        with open('Fichiers/adjacences_territoires.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
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
        index1 = graphe[0].index(territoire1.nom_territoire)+1
        index2 = graphe[0].index(territoire2.nom_territoire)
        print(graphe[index1][0])
        print(graphe[0][index2])
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
                image = pygame.transform.scale(image, (int(self.fen_width), int(self.fen_height)))
                mask = pygame.mask.from_surface(image)
                li.append(territoire(area, country, mask, image))
        return li

    def check_continent_owner(self, continent: str, player):
        """Continent prend les valeurs Europe, Asie, Amérique du Nord, Amérique du Sud, Afrique, Océanie
        """
        own_continent = True
        for i_territoire in self.liste_territoire_obj:
            if i_territoire.nom_zone == continent and i_territoire.joueur != player:
                own_continent = False
                break  # blc des conventions de codage du fimi
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
                n_territoire +=i_territoire.nombre_troupes
        return n_territoire

    def bonus(self):
        """
        Le bonus de troupe est octroyé à chaque tour à tout le monde, le nombre variant selon différent critère.
        Bonus pour le contrôle de territoire : 12-14 -> 1 régiment par territoire, 15-17 -> 2, 18-20 -> 3, 21-23 ->4,
        24-26 -> 5, 27-29 -> 6, 30-32 -> 7, 33-35 -> 8, 36-39-> 9, 40-42 -> 10
        Bonus pour le contrôle de continent : NA -> 5, SA -> 2, EU -> 5, AF -> 3, AS -> 7, OC -> 2
        """
        for player in self.liste_joueurs:
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
            type = randint(1, 8)
            # il y a peut etre un problème d'organistion la dedans entre les classes
            if type == 7:
                aim = choice(self.liste_joueurs)
                i.mission = Mission(type, i.nom, self.li_territoires_obj, aim=aim )
            else:
                i.mission = Mission(type, i.nom, self.li_territoires_obj)

    def get_player(self, str):
        for player in self.liste_joueurs:
            print(f"Dans get_player, le type de player est {type(player)}")
            print(f"{player.nom} / {str}")
            print(f"le type de player.nom est {type(player.nom)} et celui de str {type(str)}")
            if (player.nom) == (str):
                return player
        return "Joueur non trouvé"

    def changer_couleur(self, country):
        """Remplace tous les pixels de la surface avec color, garde la transparence"""
        player = country.joueur
        color = player.couleur
        width, height = country.surface.get_size()
        r, g, b = color
        for x in range(width):
            for y in range(height):
                a = country.surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                country.surface.set_at((x, y), pygame.Color(r, g, b,a))  # défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale


#A quoi ça sert ?
def tri_fusion(liste):
    """Permet de retourner la liste de scores de dés dans l'ordre décroissant """
    liste_triee = []
    liste_triee_ordre_decroissant = []
    if len(liste) <= 1:
        liste_triee = liste
    else:
        milieu = len(liste) // 2
        gauche = tri_fusion(liste[:milieu])
        droite = tri_fusion(liste[milieu:])
        liste_triee = fusion_triee(gauche, droite)
        liste_triee_ordre_decroissant = liste_triee[::-1]
    return liste_triee_ordre_decroissant


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
    def __init__(self, type:int, player:str, liste_territoire_obj,aim:str = None):
        self.type = type
        self.aim = aim #ne mettre une valeur que pour la mission 7, qui sera alors le joueur nommé
        self.player = player
        self.liste_territoire_obj = liste_territoire_obj #liste_territoire_obj est la liste de tout les objet territoire de associé à chacun des territoires de la carte

    def check(self):
        #Pourquoi il y a pas de switch case en python putain
        if self.type == 1:
            return self.check_mission1()
        elif self.type == 2:
            return self.check_mission2()
        elif self.type == 3:
            return self.check_mission3()
        elif self.type == 4:
            return self.check_mission4()
        elif self.type == 5:
            return self.check_mission5()
        elif self.type == 6:
            return self.check_mission6()
        elif self.type == 7:
            return self.check_mission7()
        elif self.type == 8:
            return self.check_mission8()

    def check_continent_owner(self, continent:str):
        """Continent prend les valeurs Europe, Asie, Amérique du Nord, Amérique du Sud, Afrique, Océanie
        """
        own_continent = True
        for i_territoire in self.liste_territoire_obj:
            if i_territoire.nom_zone == continent and i_territoire.joueur != self.player:
                own_continent = False
                break # blc des conventions de codage du fimi
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
            if i_territoire.joueur == self.player:
                n+=1
        return True if n >= 24 else False

    def check_mission7(self):
        """destroy all armies of a named opponent or,
        in the case of being the named player oneself, to capture 24 territories"""
        check = True
        if self.aim != self.player:
            for i_territoire in self.liste_territoire_obj:
                if i_territoire.joueur == self.aim and i_territoire.nombre_troupes != 0:
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
            if i_territoire.joueur == self.player and i_territoire.nombre_troupes >= 2:
                n += 1
        return True if n >= 18 else False

'''CE qu'il reste a faire : 
    - Mettre en place les différentes missions et détecter lorsque un joueur les a toutes accomplies
    - Mettre en place les bonus 
    - Créer une armée neutre pour les parties à 2 joueurs
    - Créer une classe qui définit ce qu'esst précisément un tour (le temps, les opéraitons effectuées...) 
    
    
    
    
    
    '''