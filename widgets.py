"""
Fichier contenant les widgets utiles pour l'UI du Risk.

Utilistation : `import widgets`
"""

import pygame

class selectNB:
    """
    Classe pour widget `Sélecteur de nombre`.
    Source initiale :
    https://stackoverflow.com/questions/29404502/pygame-and-spin-box

    Paramètres
    ----------
    - position <tuple> : Coordonnées de l'élément à partir du coin supérieur gauche
    - val <int> : Valeur initiale du sélecteur
    - minimum <int> : Valeur minimum que le sélecteur peut atteindre
    - maximum <int> : Valeur maximum que le sélecteur peut atteindre

    Attributs
    ---------
    - etat <int> : Valeur actuelle du sélecteur
    - pas <int> : Valeur du pas des boutons
    """
    

    def __init__(self, position : tuple, val : int, minimum : int, maximum : int):
        pygame.init()
        self.font = pygame.font.Font(None, 50)

        # Objets    
        self.rect = pygame.Rect(position, (85, 60))
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((0,0,0,0)) # Arrière plan transparent
        self.buttonRects = [pygame.Rect(50,5,30,20), pygame.Rect(50,35,30,20)]  # Liste contenant les deux boutons
        
        # Variables
        self.min = int(minimum)
        self.max = int(maximum)
        self.etat = int(val)
        self.pas = 1

    def draw(self, surface):

        # Afficher le sélecteur
        textline = self.font.render(str(self.etat), True, (255,255,255))

        self.image.fill((0,0,0,0)) # Arrière plan transparent

        # Boutons plus et moins
        pygame.draw.polygon(self.image, (255,255,255), [(55,20), (65,8), (75,20)])
        pygame.draw.polygon(self.image, (255,255,255), [(55,40), (65,52), (75,40)])

        self.image.blit(textline, (5, (self.rect.height - textline.get_height()) // 2))
        surface.blit(self.image, self.rect)

    def increment(self):
        if self.etat < self.max:
            self.etat += self.pas

    def decrement(self):
        if self.etat > self.min:
            self.etat -= self.pas

    def __call__(self, position):
        
        # Parcours des deux boutons
        for idx, btnR in enumerate(self.buttonRects):
            # Création d'un rectangle de même forme que le bouton, mais de position absolue sur l'écran, afin d'obtenir les bonnes coordonnées
            btnRect = pygame.Rect((btnR.topleft[0] + self.rect.topleft[0], btnR.topleft[1] + self.rect.topleft[1]), btnR.size)
            # Recherche du bouton cliqué
            if btnRect.collidepoint(position):
                # L'indice 0 correspond au bouton du haut
                if idx == 0:
                    return 0
                else:
                    return 1
                



class barreTexte():
    """
    Classe pour le widget `Barre de texte`
    Source initiale : Bing AI

    Paramètres
    ----------
    Args :
    - surface <pygame.Surface> : Surface sur laquelle la barre est implantée
    - position <tuple> : Position du coin supérieur droit de la barre sur `surface`
    - longueur <int> : Longueur de la barre
    - hauteur <int> : Hauteur de la barre
    Kwargs :
    - couleur_texte <tuple> : Couleur d'affichage du texte (défaut : blanc)
    - couleur_contour <tuple> : Couleur du contour de la barre (défaut : rouge)

    Attributs
    ---------
    - LONGUEUR_BARRE <int> : Longueur de la barre
    - LARGEUR_BARRE <int> : Largeur de la barre
    - COULEUR_CONTOUR <tuple> : Couleur du contour de la barre
    - COULEUR_TEXTE <tuple> : Couleur d'affichage du texte
    - POSITION <tuple> : Position du coin supérieur droit de la barre sur `surface`
    - chaine <str> : Valeur actuelle de la chaine de caractères affichée
    - surface <pygame.Surface> : Surface sur laquelle la barre est implantée
    - surface_barre pygame.Surface> : Surface contenant le contour et sur laquelle le texte est blit
    - police_obj <pygame.font.Font> : Objet pygame de la police utilisée
    """
    
    def __init__(self, surface : pygame.Surface, position : tuple, longueur : int, hauteur : int, couleur_texte : tuple = (255,255,255), couleur_contour : tuple = (255,0,0)):

        # Paramètres/Variables
        self.LONGUEUR_BARRE = int(longueur)
        self.HAUTEUR_BARRE = int(hauteur)
        self.COULEUR_CONTOUR = couleur_contour
        self.COULEUR_TEXTE = couleur_texte
        self.POSITION = position
        self.chaine = ""                                                                                    # Initialisation de la chaîne de caractères                           
        self.surface = surface                                                                              # Surface sur laquelle est implantée la battre
        self.surface_barre = pygame.Surface((self.LONGUEUR_BARRE, self.HAUTEUR_BARRE), pygame.SRCALPHA)     # Surface contenant le contour et sur laquelle le texte est blit

        # Police
        police_chemin = "./Fonts/Monocraft.ttf"
        police_taille = 19
        self.police_obj = pygame.font.Font(police_chemin, police_taille)


    def changer_texte(self, nouveau : str):
        """
        Changer le texte contenu dans la barre

        Arguments
        ---------
        - nouveau <str> : Nouveau texte
        """
        self.chaine = str(nouveau)


    def afficher_texte(self):
        """
        Afficher la barre et le texte correspondant
        """
        # Barre et contour
        self.surface_barre.fill((255,255,255,0))                                                                        # Transparence
        pygame.draw.rect(self.surface_barre, self.COULEUR_CONTOUR, [0, 0, self.LONGUEUR_BARRE, self.HAUTEUR_BARRE], 3)  # Création du contour
        self.surface.blit(self.surface_barre, self.POSITION)

        # Texte
        texte = self.police_obj.render(self.chaine, True, self.COULEUR_TEXTE)
        rect_texte = texte.get_rect(center=(self.LONGUEUR_BARRE/2, self.HAUTEUR_BARRE/2))
        self.surface_barre.blit(texte, rect_texte)
        self.surface.blit(self.surface_barre, self.POSITION)