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
    def __init__(self,nom,type, joueur,territoire):
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
        

class territoire ():
    def __init__(self, joueur,nombre_troupes,nom_zone,territoires):
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone

        
        
def attaque(territoire_attaquant, territoire_attaque):
    score_attaquant = 0
    score_attaque = 0
    gagnant = ''
    for i in range(territoire_attaquant['nombre_troupes']) : 
        score_attaquant += des()
    for i in range(territoire_attaque['nombre_troupes']):
        score_attaque += des()
    if score_attaquant<score_attaque : 
        territoire_attaquant['nombre_troupes']=0
        gagnant = territoire_attaque['joueur']
    elif score_attaquant>score_attaque : 
        territoire_attaque['nombre_troupes']=0
        gagnant = territoire_attaquant['joueur']
    else : 
        print('Oh une égalité, la bataille continue !!')
        attaque(territoire_attaquant, territoire_attaque)
    return gagnant

from random import randint
def des ():
    x = randint(1,6)
    return x
    
