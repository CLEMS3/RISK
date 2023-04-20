# -*- coding: utf-8 -*-
"""

Created on Tue Mar 28 18:53:04 2023

@author: vince
"""
from random import randint, random
import time
import json
import csv


def des():
    x = randint(1, 6)
    return x


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


class territoire():
    def __init__(self, joueur, nombre_troupes, nom_zone, nom_territoire):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone  # ce sera pour les bonus

class Game:
    def __init__(self, liste_joueurs, play_mode):
        #initialisation des variables et chargement des données
        self.liste_joueurs = liste_joueurs
        self.play_mode = play_mode
        self.graphe = self.import_adjacence()
        self.dict_territoires = self.import_territoire()
        self.li_territoires = self.liste_territoires()
        self.liste_territoires_restant = self.li_territoires
        self.tps_debut = time.time()


        #initialisation de la partie
        self.initialisation_territoires() #à voir si c'est utile
        self.placement_initial() #est ce qu'il faut faire le placement de tous les joueurs aussi ?


    def attaque(self, territoire_attaquant, territoire_attaque):
        """"
        Fonction qui gère l'attaque d'un territoire par un joueur
        A remodifier car on va pas mettre des prints
        WTF c'est censé être quoi territoire_attaquant
        """
        if self.verification_adjacence(territoire_attaquant,territoire_attaque) == True :
            scores_attaquant = []
            scores_attaque = []
            nb_des_a_comparer = territoire_attaquant['nombre_troupes'] - (territoire_attaque['nombre_troupes'] - 1)
            for i in range(territoire_attaquant['nombre_troupes']):
                scores_attaquant.append(des())

            for i in range(territoire_attaque['nombre_troupes'] - 1):
                scores_attaque.append(des())
            scores_attaquant = tri_fusion(scores_attaquant)
            scores_attaque = tri_fusion(scores_attaque)
            gagnant = 0
            while i <= nb_des_a_comparer and gagnant == 0:
                if scores_attaquant[i] <= scores_attaque[i]:
                    territoire_attaquant['nombre_troupes'] -= 1
                    territoire_attaquant['joueur']['nb_troupes']-=1
                    i += 1
                if scores_attaquant[i] > scores_attaque[i]:
                    territoire_attaque['nombre_troupes'] -= 1
                    territoire_attaque['joueur']['nb_troupes']-=1
                    i += 1
                if territoire_attaquant['nombre_troupes'] == 0:
                    territoire_attaquant['joueur']['territoires'].remove(territoire_attaquant)
                    territoire_attaque['joueur']['territoires'].append(territoire_attaquant)
                    print('Défenseur, vous vous êtes bien défendu, il ne reste plus de troupes à votre ennemi, déplacez vos troupes pour occuper son territoire!')
                    gagnant = 1
                if territoire_attaque['nombre_troupes'] == 0:
                    territoire_attaquant['joueur']['territoires'].apppend(territoire_attaque)
                    territoire_attaque['joueur']['territoires'].remove(territoire_attaque)
                    print('Attaquant, vous avez gagné un nouveau territoire, déplacez vos troupes pour l occuper')
                    gagnant = 1
        else :
            print("Vous ne pouvez pas attaquer ce territoire, il n'est pas adjacent. ")

    def import_territoire(self):
        with open('Fichiers/package.json', 'r', encoding='utf-8') as f:
            donnees_lues = json.load(f)
        return donnees_lues  # retourne un dictionnaire

    def liste_territoires(self):
        li = []
        for i in self.import_territoire().values():
            li.append(i)
        return li

    def transfert_troupes(self, territoire_de_depart, territoire_arrivee, nb_troupes_a_transferer):
        """
        Fonction qui gère le transfère de troupe d'un territoire à l'autre
        """
        if self.verification_adjacence(territoire_de_depart, territoire_arrivee) == True:
            if nb_troupes_a_transferer <= 0:
                print('Veuillez donner un nombre strictement positif de troupes à transférer')
            if nb_troupes_a_transferer < territoire_de_depart:
                territoire_de_depart['nombre_troupes'] = territoire_de_depart[
                                                             'nombre_troupes'] - nb_troupes_a_transferer
                territoire_arrivee['nombre_troupes'] += nb_troupes_a_transferer
            else:
                print(
                    'Vous ne pouvez pas transférer autant de troupes !!!!')  # il faut rajouter la condition de proximité avec la matrice d'adjacence
        else:
            print(
                "Vos territoires ne sont pas adjacents, vous ne pouvez pas transférer des troupes, sélectionnez un autre territoire")



    def placement_de_tous_les_joueurs(self, liste_joueurs):
        nb_joueurs = len(liste_joueurs)

        if nb_joueurs == 2:
            for joueur in liste_joueurs:
                self.placement_initial(joueur, 40, 14,
                                  self.liste_territoires_restant)  # il faut ajouter l'armée neutre qui a le meme nombre de territoires
        elif nb_joueurs == 3:  # et 2 régiments par territoire
            for joueur in liste_joueurs:
                self.placement_initial(joueur, 35, 14, self.liste_territoires_restant)
        elif nb_joueurs == 4:
            joueurs_chanceux = self.joueur_au_hasard(liste_joueurs)
            for joueur in liste_joueurs:
                if liste_joueurs[joueurs_chanceux[0]] == joueur or liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 30, 11, self.liste_territoires_restant)
                else:
                    self.placement_initial(joueur, 30, 10, self.liste_territoires_restant)

        elif nb_joueurs == 5:
            joueurs_chanceux = self.joueur_au_hasard(liste_joueurs)
            for joueur in liste_joueurs:
                if liste_joueurs[joueurs_chanceux[0]] == joueur or liste_joueurs[joueurs_chanceux[1]] == joueur:
                    self.placement_initial(joueur, 25, 9, self.liste_territoires_restant)
                else:
                    self.placement_initial(joueur, 25, 8, self.liste_territoires_restant)
        else:
            for joueur in liste_joueurs:
                self.placement_initial(joueur, 20, 7, self.liste_territoires_restant)

    def joueur_au_hasard(self, liste_joueurs):
        liste_indice_joueurs_selectionnes = []
        indice_joueur_selectionne_1 = -1
        indice_joueur_selectionne_2 = -1
        while indice_joueur_selectionne_1 == indice_joueur_selectionne_2:
            indice_joueur_selectionne_1 = randint(0, len(liste_joueurs) - 1)
            indice_joueur_selectionne_2 = randint(0, len(liste_joueurs) - 1)
        liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_1)
        liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_2)
        return liste_indice_joueurs_selectionnes

    def placement_initial(self, joueur, nb_troupes_a_placer, nb_territoire_a_occuper, liste_territoires_restant):
        joueur[
            'nb_troupes'] = nb_troupes_a_placer  # depend du nombre de joueurs : l'info sera à mettre sur un fichier json que l'on lira
        i = 0
        territoires_occupés_par_le_joueur = []
        nombre_de_troupes_qu_il_reste_a_placer = nb_troupes_a_placer

        while i <= nb_territoire_a_occuper:
            a = random.randint(0,(len(self.li_territoires) - 1))  # On attribue une liste de territoires a occuper par le joueur
            territoires_occupés_par_le_joueur.append(liste_territoires_restant[a])
            liste_territoires_restant.remove(liste_territoires_restant[a])
            i += 1
        joueur['territoires'] = territoires_occupés_par_le_joueur
        for territoire in territoires_occupés_par_le_joueur:
            territoire['nombre_troupes'] = 1  # On place une troupe par territoire
            nombre_de_troupes_qu_il_reste_a_placer -= 1

        while nombre_de_troupes_qu_il_reste_a_placer > 0:
            territoire_ou_il_faut_ajouter_des_troupes = territoires_occupés_par_le_joueur[
                (input("Choisissez l'indice du territoire ou il y a trop de troupes"))]
            nombre_de_troupes_a_ajouter = input("Combien de troupes voulez-vous ajouter a ce territoire ?")
            if nombre_de_troupes_a_ajouter > nombre_de_troupes_qu_il_reste_a_placer:  # Le joueur ajoute des troupes sur les territoires qu'il
                print("Il ne vous reste pas assez de troupes !!")
            else:
                territoire_ou_il_faut_ajouter_des_troupes['nombre_troupes'] += nombre_de_troupes_a_ajouter
                nombre_de_troupes_qu_il_reste_a_placer -= nombre_de_troupes_a_ajouter

        # il faut que le joueur tire des territoires au hasard où il placera ses troupes comme il le souhaite avec toujours au minimum une troupe sur chaque territoire occupé

    def import_adjacence(self):
        graphe = list(csv.reader(open("Fichiers/adjacences_territoires.csv")))
        return graphe

    def verification_adjacence(self, territoire1, territoire2):
        """
        Vérifie si deux territoires sont adjacents
        """
        i = self.li_territoires.index(territoire1)
        j = self.li_territoires.index(territoire2)
        if self.graphe[i + 1][j + 1] == 1:  # vérifier si il y a pas un décallage
            return True
        else:
            return False

    def initialisation_territoires(self):
        """
        Initialise tout les objets territoires et renvoie la liste des territoires
        """

#A quoi ça sert ?
def tri_fusion(liste):
    liste_triee = []
    if len(liste) <= 1:
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