import pygame
from pygame.locals import *
import glob

# Dossier des images de pays
PATH_PAYS='Pictures/Maps/'

# Taille de l'écran
fen_width=1280
fen_height=800

class LutinPays():
    """
    Classe des pays affichés sur la carte
    (lutin = sprite en français)
    """
    def __init__(self, surface, fichier_id):
        self.carte = surface
        self.id = fichier_id

    
def liste_pays(path_init: str, start: int, stop: int, prefix: str = ""):
    """
    Prend en argument le chemin du dossier des images des pays `path_init`,
    ainsi que la valeur initiale `start` et finale `stop` des indices dans les noms.
    Admet aussi un argument optionnel `prefix` pour les noms des pays, tel que <prefix><indice>.png

    Renvoie une liste de strings contenant les chemins des pays à afficher
    """
    out = []

    for cptr in range(start, stop + 1):
        text = path_init + prefix + str(cptr) + ".png"
        out.append(str(text))

    return out

# Ecrire la fonction pour changer la couleur des images de pays
# https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen
def changer_couleur(surface, color):
    """Remplace tous les pixels de la surface avec color, garde la transparence"""
    width, height = surface.get_size()
    r, g, b, _ = color
    for x in range(width):
        for y in range(height):
            a = surface.get_at((x, y))[3] #obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
            surface.set_at((x, y), pygame.Color(r, g, b, a)) #défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale

class Fenetre():
    def __init__(self,fenetre): 
        self.fenetre = fenetre
        self.surfaces = []          # Liste des surfaces à afficher sur la surface de la fenêtre
    
    def afficher(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """
        pays_liste = liste_pays(PATH_PAYS, 1, 42)

        for cptr, pays in enumerate(pays_liste):
            image = pygame.image.load(pays).convert()                             # Chargement des images et convert pour optimiser l'affichage
            # coeff = (int(fen_width/image.get_width()), int(fen_height/image.get_width()))
            image = pygame.transform.scale(image, int(fen_width), int(fen_height))
            lutin = LutinPays(image, int(cptr+1))
            # Appliquer le masque de couleur ici
            changer_couleur(image)
