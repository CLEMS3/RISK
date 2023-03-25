import tkinter as tk
from tkinter import scrolledtext
import csv
import math
import random

# penser à clearer la textArea après un usage et réinit des variables

class Fenetre_avec_graphique():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique")
        self.racine.resizable(height = False, width = False)
        self.R = 6378.000 # Rayon de la terre en km 

        #création des attributs autour du dico 
        self.dicoSommets = {} # dico des sommets avec leur position (structure de travail)
        self.seuil = 0.0 
        self.distance_max = 0.0
        self.distance_min = 0.0
        
        # Lecture des données vers le dictionnaire et 
        # positionnement des variables distance_min et distance_max (pour le slider)
        self.fichier = 'villes_extrait.csv'        
        self.creer_dico()
        self.distance_min_max()
        
        ########################################
        # Attributs liés à l'affichage graphique
        ########################################
        
        # Dimensions du canevas de dessin de la fenêtre d'affichage
        self.f_graph_height = 650
        self.f_graph_width = 650

        # Calcul des coordonnées cartésiennes min et max des villes du dictionnaire 
        # dans le repère d'affichage (nécessaires pour le changement de coordonnées)
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0
        self.calcul_min_max_xy()
        
        # Décalages pour élargir le cadre d'affichage
        self.offset_earth = 100
        self.offset_screen = 50

        # Fenêtre d'affichage
        self.f_graph = None
        
        self.couleur = ["black", "red", "green", "blue", "yellow", "magenta","cyan", "white", "purple"]
        self.dicoSommetsGraphiques = {} # récupère les id des sommet dessinés sur le canevas
        
        # création des widgets
        self.creer_widgets(self.racine)

    def creer_widgets(self,root):
       
        self.bouton_quitter = tk.Button(root, text="Quitter", bg='lightyellow')
        self.bouton_quitter.bind('<Button-1>', self.quitter)
        self.bouton_quitter.pack(fill = 'x', side=tk.BOTTOM)
       
        # création de la zone scrolledText avec scrall bar dans laquelle les informations seront intégrées
        self.text_area = scrolledtext.ScrolledText(root, wrap = tk.WORD, width = 50, height = 20, font = ("Times New Roman", 14))
        self.text_area.pack(side=tk.LEFT)
        self.text_area.insert(tk.INSERT,"Quelques statistiques sur les villes :" +'\n')
        self.text_area.insert(tk.INSERT,"-------------------------------------------" +'\n')
 
        # checkbox STATS
        self.stat = tk.Label(root, text = "Descripteurs", font='Helvetica 9 bold')
        self.stat.pack(anchor = tk.CENTER)
        
        self.nbSommets = tk.Button(root, text = "Nombre de villes")
        self.nbSommets.bind('<Button-1>', self.denombre_sommets)
        self.nbSommets.pack(anchor = tk.CENTER)
        
        self.distanceMoy = tk.Button(root, text = "Distance moyenne (km)")
        self.distanceMoy.bind('<Button-1>', self.distance_moyenne)
        self.distanceMoy.pack(anchor = tk.CENTER)       
        
        # scroller SEUIL
        self.var = tk.DoubleVar()
        self.scale = tk.Scale(root, orient='horizontal', from_=int(self.distance_min), to=int(self.distance_max),resolution=10, tickinterval=100, length=200, variable = self.var, font=("Calibri", 8))
        self.scale.pack(anchor = tk.W, fill = 'x')

        self.areteSelonSeuil = tk.Button(root, text = "Villes reliées selon seuil (km)  ")
        self.areteSelonSeuil.bind('<Button-1>', self.ville_distance_seuil)
        self.areteSelonSeuil.pack(anchor = tk.CENTER)         

        # Affichage de la nouvelle fenêtre       
        self.b_graphe = tk.Button(root, text = "Graphe des villes", height = 1, width = 19)
        self.b_graphe.bind('<Button-1>', self.dessine_graphe)
        self.b_graphe.pack(fill = 'x',side = tk.BOTTOM)
        self.dessin = tk.Label(root, text = "\nFenêtre graphique ", font='Helvetica 9 bold')
        self.dessin.pack(anchor = tk.CENTER, side = tk.BOTTOM)


    def creer_dico(self): 
        """
        créer le dico
        :paramètres:
        :return:
        """
        with open(self.fichier, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            sommets = {}
            for ligne in reader:
                ident, nom, lat, long, haut = ligne
                if ident not in sommets: # si la clef n'existe pas encore
                    sommets[ident] = [nom,float(lat),float(long),int(haut)]
        self.dicoSommets = sommets


    def distance_min_max(self):
        dico_temp = self.dicoSommets.copy()
        dMax = -math.inf
        dMin = math.inf
        for idv_a, [nom_a, lat_a, lng_a, h_a] in self.dicoSommets.items():
            dico_temp.pop(idv_a)
            for nom_b, lat_b, lng_b, h_b in dico_temp.values():
                d = self.distanceKm(lat_a, lng_a, lat_b, lng_b)
                if d > dMax :
                    dMax = d
                if d < dMin :
                    dMin = d
        self.distance_max = dMax
        self.distance_min = dMin


    def quitter(self, event):
       self.racine.destroy()
 
       
    def denombre_sommets(self, event):
        nbSommets = len (self.dicoSommets)
        texte = "* le nombre de villes est : " + str(nbSommets)+'\n'
        self.text_area.insert(tk.INSERT,texte)


    def distance_moyenne(self,event):
        dico_temp = self.dicoSommets.copy()
        somme = 0
        n = len(self.dicoSommets)
        for idv_a, [nom_a, lat_a, lng_a, h_a] in self.dicoSommets.items():
            dico_temp.pop(idv_a)
            for nom_b, lat_b, lng_b, h_b in dico_temp.values():
                d = self.distanceKm(lat_a, lng_a, lat_b, lng_b)
                somme += d
        moyenne = 2*somme / (n*(n-1))
        texte = f"* la moyenne des distances vaut : {moyenne:.2f} km \n"
        self.text_area.insert(tk.INSERT,texte)


    def ville_distance_seuil(self, event):
        self.seuil = self.var.get()

        self.text_area.delete("1.0", "end")
        texte = f"Voici les villes de distance à vol d'oiseau < à {self.seuil:.2f} km: \n"
        self.text_area.insert (tk.INSERT,texte)
        
        for nom_a, lat_a, long_a, haut_a in self.dicoSommets.values():
            texte = f"A partir de {nom_a} : \n"
            self.text_area.insert (tk.INSERT,texte)
            for nom_b, lat_b, long_b, haut_b in self.dicoSommets.values():
                if (nom_a != nom_b) :
                    d = self.distanceKm(lat_a, long_a, lat_b, long_b)
                    if (d <= self.seuil) :
                        texte = f" --> {nom_b} à distance de {d:.2f} km \n"
                        self.text_area.insert(tk.INSERT,texte)

    
  ##########################################################
  ##########################################################
  # Partie graphique : on dessine le graphe des villes 
  ##########################################################
  ##########################################################
  
  ###############################
  ##### Changement de référentiel
  ##### et calcul des distances
  ###############################

    def calcul_min_max_xy(self):
        '''
        
        détermine les coordonnées min et max en y et y des villes dans le plan du canevas
        et met à jour les attributs les représentant en conséquence
        Parameters
        ----------
        None

        Returns
        -------
        None.

        '''
        x_min = math.inf
        x_max = -math.inf
        y_min = math.inf
        y_max = -math.inf
        
        for nom, lat, lng, h in self.dicoSommets.values():
            x_test, y_test = self.xy_from_lat_long(lat, lng)
            if x_test < x_min :
                x_min = x_test
            if x_test > x_max :
                x_max = x_test
            if y_test < y_min :
                y_min = y_test
            if y_test > y_max :
                y_max = y_test

        self.x_min = x_min
        self.x_max = x_max 
        self.y_min = y_min
        self.y_max = y_max
            

    def xy_from_lat_long(self, latitude, longitude):
        '''
        Conversion de la latitude et longitude en coordonnées x-y plan du canevas sans normalisation
        Parameters
        ----------
        latitude : float
            valeur de la latitude en degrés
        longitude : float
            valeur de la longitude en degrés

        Returns
        -------
        x, y: float, float
            valeurs approchées des coordonnées en x et y dans le plan du canevas.

        '''
        longitude = longitude + 180
        x = ((longitude * self.f_graph_width)/360)
        
        latitude = latitude + 90
        hauteur = (latitude * self.f_graph_height)/180 
        y = self.f_graph_height - hauteur
        
        return x, y
    
    
    def xy_repere_cartesien(self, latitude, longitude, offset1, offset2):
        '''
        fonction qui effectue le changement de repère complet de la longitude d'une ville
        à sa position normalisée dans le repère (x,y) du canevas veillant à respecter les bordures

        Parameters
        ----------
        latitude : float
            valeur de la latitude en degrés
        longitude : float
            valeur de la longitude en degrés
        offset1 : int
            décalage assurant un retrait en bordure droite
        offset2 : int
            décalage assurant un retrait en bordure gauche

        Returns
        -------
        x, y : float
            valeurs des coordonnées normalisée dans le plan du canevas

        '''
        x_ville, y_ville = self.xy_from_lat_long(latitude, longitude)
                        
        x = (self.f_graph_width - offset1) / (self.x_max - self.x_min) * (x_ville - self.x_min) + offset2
        y = (self.f_graph_height - offset1) / (self.y_max - self.y_min) * (y_ville - self.y_min) + offset2 
        
        return x, y


  ##############################################
  ### calcul de distance dans le bon référentiel
  ##### du GPS au cartésien
  #### changement de référentiel
  ##############################################

    #Conversion des degrés en radian
    def convertRad(self, val_degre):
        """
        Convertir une valeur passé en degrés en radian
        - val_degre(float): la valeur à conversir en degrés
        Retour:
        - la valeur en radian (float)
        """
        return (math.pi * val_degre) / 180

    def distanceKm(self,lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre):
        """
        Calculer la distance  en km entre deux lieux repérées par leurs coordonnées GPS 
        - lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre (float): les 4 coordonnées des deux emplacements en degrés (latitude, longitude)
        Retour:
        - la valeur de la distance réelle ramenée à la surface de la terre (valeur approchée) en float
        """
        lat_a = self.convertRad(lat_a_degre)
        lon_a = self.convertRad(lon_a_degre)
        lat_b = self.convertRad(lat_b_degre)
        lon_b = self.convertRad(lon_b_degre)
        distKm = self.R * (math.pi/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))
        return distKm

    def distance (self, x0, y0, x1, y1):
        return math.sqrt ((x1-x0)**2+(y1-y0)**2)        
            
  
  ##########################################################
  # Les fonctions de dessins : sommet et arêtes
  ##########################################################
  
    def dessine_graphe(self, event):
      if (self.f_graph != None) :
          self.f_graph.destroy()
      self.f_graph = tk.Toplevel(self.racine)
      self.f_graph.resizable(height = False, width = False)
      self.f_graph.canevas = tk.Canvas(self.f_graph, bg="light blue", height=self.f_graph_height, width=self.f_graph_width)
      self.f_graph.canevas.pack()
      self.dessine_sommets()
      self.dessine_arcs()


    def dessine_sommets(self):       
        rayon=5
        for nom, lat, lng, h in self.dicoSommets.values():
            x, y = self.xy_repere_cartesien(lat, lng, self.offset_earth, self.offset_screen)
            id_text = self.f_graph.canevas.create_text(x, y-2*rayon)
            self.f_graph.canevas.itemconfigure(id_text, text = nom)
            color = self.couleur[random.randint(0,len(self.couleur)-1)]
            item = self.f_graph.canevas.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, fill = color)
            self.dicoSommetsGraphiques[item] = nom
            self.f_graph.canevas.tag_bind(item, '<Button-1>', self.affiche_info_ville)

            
    def dessine_arcs(self):
        self.seuil= self.var.get()
        
        dico_tmp = self.dicoSommets.copy()
         
        for id_a, [nom_a, lat_a, lng_a, h_a] in self.dicoSommets.items():
            xi, yi = self.xy_repere_cartesien(lat_a, lng_a, self.offset_earth, self.offset_screen)
            dico_tmp.pop(id_a)
            for nom_b, lat_b, lng_b, h_b in dico_tmp.values():
                d = self.distanceKm(lat_a, lng_a, lat_b, lng_b)
                xj, yj = self.xy_repere_cartesien(lat_b, lng_b, self.offset_earth, self.offset_screen)
                if d <= self.seuil:
                    self.f_graph.canevas.create_line(int(xi), int(yi), int(xj), int(yj), fill="blue")
            
  ##########################################################
  # Interactions au clic de souris => affiche info
  ##########################################################

    def affiche_info_ville(self,event):
        self.text_area.delete("1.0", "end")
        item_clicked = self.f_graph.canevas.find_withtag("current")[0]
        texte = f"La ville sélectionnée est: {self.dicoSommetsGraphiques[item_clicked]} " +'\n'
        self.text_area.insert(tk.INSERT,texte)


    
if __name__ == "__main__":
    app = Fenetre_avec_graphique()
    app.racine.mainloop()
