# -*- coding: utf-8 -*-
"""

Created on Tue Mar 28 18:53:04 2023

@author: vince
"""
from random import randint

def des() : 
    x = randint(1,6)
    return x

class troupes ():
    def __init__(self,nom,type,joueur,territoire):
        self.nom = nom
        self.type = type
        self.joueur = joueur
        self.territoire = territoire
        
        
class mission () : 
    def __init__(self, zone, joueur, nom, description,etat):
        self.nom = nom
        self.joueur = joueur
        self.zone= zone
        self.description = description
        self.etat = etat     #l'etat est un attribut pour distinguer lorsque la mission
                             #est accomplie
    def mission_accomplie (zone):
        if zone['joueurs'] == ['joueur'] : 
            etat = 'accomplie'

class territoire ():
    def __init__(self, joueur,nombre_troupes,nom_zone,nom_territoire):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone

        
        
def attaque(territoire_attaquant, territoire_attaque):
    scores_attaquant = []
    scores_attaque = []
    nb_des_a_comparer = territoire_attaquant['nombre_troupes'] - territoire_attaque['nombre_troupes']
    for i in range (territoire_attaquant['nombre_troupes']) : 
        scores_attaquant.append(des())
    
    for i in range (territoire_attaque['nombre_troupes']) : 
        scores_attaque.append(des())
    scores_attaquant = tri_fusion(scores_attaquant)
    scores_attaque = tri_fusion(scores_attaque)
    gagnant = 0
    while i <= nb_des_a_comparer and gagnant == 0 :
        if scores_attaquant[i]<=scores_attaque[i] : 
            territoire_attaquant['nombre_troupes']-=1
            i+=1
        if scores_attaquant[i]>scores_attaque[i] : 
            territoire_attaque['nombre_troupes']-=1
            i+=1
        if territoire_attaquant['nombre_troupes']== 0 or territoire_attaque['nombre_troupes'] == 0 :
            gagnant = 1



def tri_fusion(liste):
    liste_triee = []
    if len(liste)<=1:
        liste_triee = liste
    else : 
        milieu = len(liste)//2
        gauche = tri_fusion(liste[:milieu])
        droite = tri_fusion(liste[milieu:])
        liste_triee = fusion_triee(gauche, droite)
    return liste_triee

def fusion_triee(liste1, liste2):
    resultat = []
    i = j = 0
    while i< len(liste1) and j < len(liste2) : 
        if liste1[i] < liste2[j] : 
            resultat.append(liste1[i])
            i+=1
        else : 
            resultat.append(liste2[j])
            j+=1
    resultat.extend(liste1[i:] or liste2[j:])
    return resultat

    


def transfert_troupes (territoire_de_depart,territoire_arrivee,nb_troupes_a_transferer):
    territoire_de_depart['nombre_troupes'] = territoire_de_depart['nombre_troupes'] - nb_troupes_a_transferer
    territoire_arrivee['nombre_troupes'] += nb_troupes_a_transferer
