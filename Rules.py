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


class timer:

    def __init__(self, duree):
        self.reference = time.time()
        self.duree = duree

    def temps_restant(self):
        return self.reference - (time.time() - self.reference)


class troupes():
    def __init__(self, nom, type, joueur, territoire):
        self.nom = nom
        self.type = type
        self.joueur = joueur
        self.territoire = territoire


# Les missions seront en fonction du nombre de joueurs et du temps approximatifs de la partie à laquelle ils veulent jouer
# exemple : si il  y a 3 joueurs qui veulent jouer 10 minutes : ils doivent conquérir 15 territoires avec au moins 2 troupes par territoires
class mission():
    def __init__(self, zone, joueur, nom, description, nb_territoires_pour_mission, etat, nb_troupes_sur_territoires):
        self.nom = nom
        self.joueur = joueur
        self.nb_territoires_pour_mission = nb_territoires_pour_mission
        self.nb_troupes_sur_territoires = nb_troupes_sur_territoires
        self.description = description
        self.etat = etat  # l'etat est un attribut pour distinguer lorsque la mission
        # est accomplie

    def mission_accomplie(joueur, mission):
        for territoire_occupe in joueur['territoires_que_le_joueur_occupe']:
            if joueur['nb_territoires_du_joueurs'] >= mission['nb_territoires_pour_mission'] and territoire_occupe[
                'nombre_troupes'] >= mission['nb_troupes_sur_territoires']:
                mission['etat'] = 'accomplie'

                # pour e+repérer si un joueur a gagné la partie on doit vérifier que toutes les missions qu'il a sont terminées (à lier à la classe joueur)


# class bonus() :
# a faire quand les autres trucs marcheront


class territoire():
    def __init__(self, joueur, nombre_troupes, nom_zone, nom_territoire):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone  # ce sera pour les bonus


def attaque(territoire_attaquant, territoire_attaque):
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
            i += 1
        if scores_attaquant[i] > scores_attaque[i]:
            territoire_attaque['nombre_troupes'] -= 1
            i += 1
        if territoire_attaquant['nombre_troupes'] == 0:
            gagnant = 1
            print(
                'Défenseur, vous vous êtes bien défendu, il ne reste plus de troupes à votre ennemi, déplacez vos troupes pour occuper son territoire!')
        if territoire_attaque['nombre_troupes'] == 0:
            gagnant = 1
            print('Attaquant, vous avez gagné un nouveau territoire, déplacez vos troupes pour l occuper')


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


def transfert_troupes(territoire_de_depart, territoire_arrivee, nb_troupes_a_transferer):
    if nb_troupes_a_transferer <= 0:
        print('Veuillez donner un nombre strictement positif de troupes à transférer')
    if nb_troupes_a_transferer < territoire_de_depart:
        territoire_de_depart['nombre_troupes'] = territoire_de_depart['nombre_troupes'] - nb_troupes_a_transferer
        territoire_arrivee['nombre_troupes'] += nb_troupes_a_transferer
    else:
        print(
            'Vous ne pouvez pas transférer autant de troupes !!!!')  # il faut rajouter la condition de proximité avec la matrice d'adjacence


def import_territoire():
    with open('Fichiers/package.json', 'r', encoding='utf-8') as f:
        donnees_lues = json.load(f)
    return donnees_lues  # retourne un dictionnaire


def liste_territoires():
    li = []
    for i in import_territoire().values():
        li.append(i)
    return li

liste_territoires_restant = liste_territoires()
def placement_de_tous_les_joueurs(liste_joueurs):
    nb_joueurs = len(liste_joueurs)

    if nb_joueurs == 2:
        for joueur in liste_joueurs:
            placement_initial(joueur, 40, 14,
                              liste_territoires_restant)  # il faut ajouter l'armée neutre qui a le meme nombre de territoires
    elif nb_joueurs == 3:  # et 2 régiments par territoire
        for joueur in liste_joueurs:
            placement_initial(joueur, 35, 14, liste_territoires_restant)
    elif nb_joueurs == 4:
        for joueur in liste_joueurs:
            joueurs_chanceux = joueur_au_hasard(liste_joueurs)
            if liste_joueurs[joueurs_chanceux[0]] == joueur or liste_joueurs[joueurs_chanceux[1]] == joueur:
                placement_initial(joueur, 30, 11, liste_territoires_restant)
            else:
                placement_initial(joueur, 30, 10, liste_territoires_restant)

    elif nb_joueurs == 5:
        for joueur in liste_joueurs:
            joueurs_chanceux = joueur_au_hasard(liste_joueurs)
            if liste_joueurs[joueurs_chanceux[0]] == joueur or liste_joueurs[joueurs_chanceux[1]] == joueur:
                placement_initial(joueur, 25, 9, liste_territoires_restant)
            else:
                placement_initial(joueur, 25, 8, liste_territoires_restant)
    else:
        for joueur in liste_joueurs:
            placement_initial(joueur, 20, 7, liste_territoires_restant)


def joueur_au_hasard(liste_joueurs):
    liste_indice_joueurs_selectionnes = []
    indice_joueur_selectionne_1 = -1
    indice_joueur_selectionne_2 = -1
    while indice_joueur_selectionne_1 == indice_joueur_selectionne_2:
        indice_joueur_selectionne_1 = randint(0, len(liste_joueurs) - 1)
        indice_joueur_selectionne_2 = randint(0, len(liste_joueurs) - 1)
    liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_1)
    liste_indice_joueurs_selectionnes.append(indice_joueur_selectionne_2)
    return liste_indice_joueurs_selectionnes


def placement_initial(joueur, nb_troupes_a_placer, nb_territoire_a_occuper, liste_territoires_restant):
    joueur[
        'nb_troupes'] = nb_troupes_a_placer  # depend du nombre de joueurs : l'info sera à mettre sur un fichier json que l'on lira
    i = 0
    territoires_occupés_par_le_joueur = []
    nombre_de_troupes_qu_il_reste_a_placer = nb_troupes_a_placer

    while i <= nb_territoire_a_occuper:
        a = random.randint(0,
                           (len(liste_territoires) - 1))  # On attribue une liste de territoires a occuper par le joueur
        territoires_occupés_par_le_joueur.append(liste_territoires_restant[a])
        liste_territoires_restant.remove(liste_territoires_restant[a])
        i += 1

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

def import_adjacence():
    graphe = list(csv.reader(open("Fichiers/adjacences_territoires.csv")))
    return graphe

graphe = import_adjacence()

def verification_adjacence(territoire1, territoire2):
    i = liste_territoires().index(territoire1)
    j = liste_territoires().index(territoire2)
    if graphe[i+1][j+1] == 1: #vérifier si il y a pas un décallage
        return True
    else:
        return False
