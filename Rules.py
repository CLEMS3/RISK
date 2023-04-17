# -*- coding: utf-8 -*-
"""

Created on Tue Mar 28 18:53:04 2023

@author: vince
"""
from random import randint, random
import time
def des() : 
    x = randint(1,6)
    return x


class timer:

    def __init__(self, duree):
        self.reference = time.time()
        self.duree = duree

    def temps_restant(self):
        return self.reference - (time.time() - self.reference)





class troupes ():
    def __init__(self,nom,type,joueur,territoire):
        self.nom = nom
        self.type = type
        self.joueur = joueur
        self.territoire = territoire
        
#Les missions seront en fonction du nombre de joueurs et du temps approximatifs de la partie à laquelle ils veulent jouer
# exemple : si il  y a 3 joueurs qui veulent jouer 10 minutes : ils doivent conquérir 15 territoires avec au moins 2 trouês par territoires        
class mission () : 
    def __init__(self, zone, joueur, nom, description,nb_territoires_pour_mission,etat,nb_troupes_sur_territoires):
        self.nom = nom
        self.joueur = joueur
        self.nb_territoires_pour_mission = nb_territoires_pour_mission
        self.nb_troupes_sur_territoires = nb_troupes_sur_territoires
        self.description = description
        self.etat = etat     #l'etat est un attribut pour distinguer lorsque la mission
                             #est accomplie
    def mission_accomplie (joueur,mission):
        for territoire_occupe in joueur['territoires_que_le_joueur_occupe'] : 
            if joueur['nb_territoires_du_joueurs']>=mission['nb_territoires_pour_mission'] and territoire_occupe['nombre_troupes']>= mission['nb_troupes_sur_territoires'] : 
                mission['etat'] = 'accomplie'

                #pour e+repérer si un joueur a gagné la partie on doit vérifier que toutes les missions qu'il a sont terminées (à lier à la classe joueur)


#class bonus() : 
#a faire quand les autres trucs marcheront




class territoire ():
    def __init__(self, joueur,nombre_troupes,nom_zone,nom_territoire):
        self.nom_territoire = nom_territoire
        self.joueur = joueur
        self.nombre_troupes = nombre_troupes
        self.nom_zone = nom_zone    # ce sera pour les bonus

        
        
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
        if territoire_attaquant['nombre_troupes']== 0 : 
            gagnant = 1
            print('Défenseur, vous vous êtes bien défendu, il ne reste plus de troupes à votre ennemi, déplacez vos troupes pour occuper son territoire!')
        if territoire_attaque['nombre_troupes'] == 0 :
            gagnant = 1
            print('Attaquant, vous avez gagné un nouveau territoire, déplacez vos troupes pour l occuper')



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
    if nb_troupes_a_transferer<=0 : 
        print('Veuillez donner un nombre strictement positif de troupes à transférer')
    if nb_troupes_a_transferer < territoire_de_depart : 
        territoire_de_depart['nombre_troupes'] = territoire_de_depart['nombre_troupes'] - nb_troupes_a_transferer
        territoire_arrivee['nombre_troupes'] += nb_troupes_a_transferer
    else : 
        print('Vous ne pouvez pas transférer autant de troupes !!!!')    # il faut rajouter la condition de proximité lorsque l'on est dans la partie après le placement








liste_territoires = ledictionnaireissudefichierjsondeCLEMENT.keys()      # CLEMENT, EST CE QUE TU PEUX ARRANGER CETTE PARTIE ????? Il faut que ce soit la liste 
                                                                        # des territoires qui ne sont pas encore occupés par les autres joueurs au début de la partie


def placement_initial(joueur,nb_troupes_a_placer,nb_territoire_a_occuper): 
    joueur['nb_troupes']= nb_troupes_a_placer          #depend du nombre de joueurs : l'info sera à mettre sur un fichier json que l'on lira
    i=0
    territoires_occupés_par_le_joueur=[]
    nombre_de_troupes_qu_il_reste_a_placer = nb_troupes_a_placer


    while i <=nb_territoire_a_occuper : 
        a=random.randint(0,(len(liste_territoires)-1))                      #  On attribue une liste de territoires a occuper par le joueur
        territoires_occupés_par_le_joueur.append(liste_territoires[a])
        liste_territoires.remove(liste_territoires[a])
        i+=1

    for territoire in territoires_occupés_par_le_joueur : 


        if nombre_de_troupes_qu_il_reste_a_placer > 0 : 

            nb_troupes_a_placer_sur_ce_territoire = input("Combien du troupes voulez-vous placer sur ce territoire ?")
            if nb_troupes_a_placer_sur_ce_territoire <=0 : 
                print("Vous devez avoir des troupes sur chaque territoire !!")
                nb_troupes_a_placer_sur_ce_territoire = input("Combien du troupes voulez-vous placer sur ce territoire ?")
            elif nb_troupes_a_placer_sur_ce_territoire > nombre_de_troupes_qu_il_reste_a_placer : 
                print("Vous ne pouvez pas placer autant de troupes !! ")
                nb_troupes_a_placer_sur_ce_territoire = input("Combien du troupes voulez-vous placer sur ce territoire ?")
            elif nb_troupes_a_placer_sur_ce_territoire >0 : 
                territoire['nommbre_troupes'] = nb_troupes_a_placer_sur_ce_territoire
                nombre_de_troupes_qu_il_reste_a_placer-=nb_troupes_a_placer_sur_ce_territoire



        if nombre_de_troupes_qu_il_reste_a_placer == 0 :

            territoire_ou_il_y_a_trop_de_troupes = territoires_occupés_par_le_joueur(input("Choisissez l'indice du territoire ou il y a trop de troupes"))
            if territoire_ou_il_y_a_trop_de_troupes['nombre_troupes'] == 0 : 
                print("Vous n'avez pas encore placé de troupes sur ce territoires")
                territoire_ou_il_y_a_trop_de_troupes = territoires_occupés_par_le_joueur(input("Choisissez l'indice du territoire ou il y a trop de troupes"))
            elif territoire_ou_il_y_a_trop_de_troupes['nombre_troupes'] == 1 : 
                print('Il n y a qu une troupe sur ce territoire, vous ne pouvez pas la transférer')
                territoire_ou_il_y_a_trop_de_troupes = territoires_occupés_par_le_joueur(input("Choisissez l'indice du territoire ou il y a trop de troupes"))
            elif territoire_ou_il_y_a_trop_de_troupes['nombre_troupes']>=2 : 
                nb_troupes_a_transferer = input ("Combien de troupes voulez-vous transférer ? ")
                if nb_troupes_a_transferer >= territoire_ou_il_y_a_trop_de_troupes['nombre_troupes'] :
                    print("Vous ne pouvez pas transférer autant de troupes, sinon vous laisserez un territoire complètement sans défense")
                    nb_troupes_a_transferer = input ("Combien de troupes voulez-vous transférer ? ")
                elif nb_troupes_a_transferer < territoire_ou_il_y_a_trop_de_troupes['nombre_troupes'] : 
                    transfert_troupes (territoire_ou_il_y_a_trop_de_troupes,territoire,nb_troupes_a_transferer)
                


    # il faut que le joueur tire des territoires au hasard où il placera ses troupes comme il le souhaite avec toujours au minimum une troupe sur chaque territoire occupé
