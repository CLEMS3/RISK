import pygame
from pygame.locals import *
import glob
from random import randint
import time



class LutinPays():
    """
    Classe des pays affichés sur la carte
    (lutin = sprite en français)
    """
    def __init__(self, surface, fichier_id):
        self.carte = surface
        self.id = fichier_id


class PygameWindow(pygame.Surface):
    def __init__(self, size):
        super().__init__(size) #sert à éviter un problème d'héritage de classe
        pygame.init()
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption("Risk - Game")
        # Dossier des images de pays
        self.PATH_PAYS = 'Pictures/Maps/'
        # Taille de l'écran
        self.fen_width = 1280
        self.fen_height = 800

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.afficher_carte()
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill((randint(0,255), randint(0,255), randint(0,255)))

            # update the window
            pygame.display.update()

    def afficher_carte(self):
        """
        Affiche les pays sur la surface de la fenêtre
        """
        pays_liste = self.liste_pays(self.PATH_PAYS, 1, 42)
        debug = 0
        for cptr, pays in enumerate(pays_liste):
            debug +=1
            print(debug)
            image = pygame.image.load(pays).convert_alpha()  # Chargement des images et convert pour optimiser l'affichage
            # coeff = (int(fen_width/image.get_width()), int(fen_height/image.get_width()))
            image = pygame.transform.scale(image, (int(self.fen_width), int(self.fen_height)))
            lutin = LutinPays(image, int(cptr+1))
            # Appliquer le masque de couleur ici
            ref = time.time()
            self.changer_couleur(image,(255, 255, 255)) #pour le moment on met tout en blanc, on mettra selon la couleur de la zone plus tard
            print(time.time()-ref)
            self.window.blit(image, (0,0))


    def liste_pays(self, path_init: str, start: int, stop: int, prefix: str = ""):
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

    def changer_couleur(self, surface, color):
        """Remplace tous les pixels de la surface avec color, garde la transparence"""
        width, height = surface.get_size()
        r, g, b = color
        for x in range(width):
            for y in range(height):
                a = surface.get_at((x, y))[3]  # obtient la valeur de la couleur de ce pixel, et le [3] prend donc le 4ème élement, ce qui correspond à la valeur de transparence du pixel
                surface.set_at((x, y), pygame.Color(r, g, b,a))  # défini la couleur du pixel selon les valeurs de rgb donné en paramètre, et avec la valeur de transparence initiale