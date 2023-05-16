"""
Fichier contenant les widgets utiles pour l'UI du Risk.

Utilistation : `import widgets`
"""
import pygame
import time



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
        """
        Dessine le sélecteur sur la `surface`
        """
        # Afficher le sélecteur
        textline = self.font.render(str(self.etat), True, (255,255,255))

        self.image.fill((0,0,0,0)) # Arrière plan transparent

        # Boutons plus et moins
        pygame.draw.polygon(self.image, (255,255,255), [(55,20), (65,8), (75,20)])
        pygame.draw.polygon(self.image, (255,255,255), [(55,40), (65,52), (75,40)])

        self.image.blit(textline, (5, (self.rect.height - textline.get_height()) // 2))
        surface.blit(self.image, self.rect)


    def increment(self):
        """
        Incrémente le sélecteur de `pas` si le `max` n'est pas encore atteint.
        """
        if self.etat <= (self.max - self.pas):
            self.etat += self.pas


    def decrement(self):
        """
        Décrémente le sélecteur de `pas` si le `min` n'est pas encore atteint.
        """
        if self.etat >= (self.min + self.pas):
            self.etat -= self.pas


    def __call__(self, position):
        """
        Fonction d'appel de l'objet, vérifie si le clic (sur `position`) a été effectué sur un des boutons

        Renvoie
        -------
        - 0 : si le bouton du haut est cliqué
        - 1 : si le bouton du bas est cliqué
        """
        
        # Parcours des deux boutons
        for idx, btnR in enumerate(self.buttonRects):
            # Création d'un rectangle de même forme que le bouton, mais de position absolue sur l'écran, afin d'obtenir les bonnes coordonnées
            btnRect = pygame.Rect((btnR.topleft[0] + self.rect.topleft[0], btnR.topleft[1] + self.rect.topleft[1]), btnR.size)
            # Recherche du bouton cliqué
            if btnRect.collidepoint(position):  # Si on a cliqué quelque part dans `btnRect`
                # L'indice 0 correspond au bouton du haut 
                return 0 if idx == 0 else 1
                


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
    - der_pas_err <str> : Dernier messages affiché (par opposition à une erreur)
    - err <bool> : Affiche-t-on actuellement une erreur ?
    - err_temps <float> : Temps depuis l'affichage de la dernière erreur
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
        self.der_pas_err = ""                                                                               # Dernier message affiché n'étant pas une erreur   
        self.err = False                                                                                    # Le message actuellement affiché est-il une erreur ?  
        self.err_temps = 0                                                                                  # Temps écoulé depuis l'erreur                  
        self.surface = surface                                                                              # Surface sur laquelle est implantée la battre
        self.surface_barre = pygame.Surface((self.LONGUEUR_BARRE, self.HAUTEUR_BARRE), pygame.SRCALPHA)     # Surface contenant le contour et sur laquelle le texte est blit

        # Police
        police_chemin = "./Fonts/Monocraft.ttf"
        police_taille = 19
        self.police_obj = pygame.font.Font(police_chemin, police_taille)


    def changer_texte(self, nouveau : str, err : bool = False, forceupdate : bool = False):
        """
        Changer le texte contenu dans la barre

        Arguments
        ---------
        - nouveau <str> : Nouveau texte
        - err <bool> : Le message est-il une erreur ?
        - forceupdate <bool> : Si True, rafraîchit la fenêtre en plus de mettre à jour le texte
        """
        # Si erreur, on stocke la dernière chaîne valide
        if err == True:
            self.err_temps = time.time()
            self.der_pas_err = self.chaine if (self.err == False) else self.der_pas_err # Si on vient de passer une erreur, on garde le dernier message, si c'était déjà une erreur, on change rien
            self.err = True
        elif (err == False) and (self.err == True): # Si on passe un message, et qu'on était en mode erreur, alors on considère le message comme le nouveau dernier message valide
            self.err = False
            self.der_pas_err = nouveau
        else:
            self.der_pas_err = nouveau              # Pareil

        # Mise à jour de la chaîne
        self.chaine = str(nouveau)

        # Si mode forcer le rafraîchissement, on rafraîchit
        if forceupdate == True:
            self.afficher_texte()
            pygame.display.update()


    def afficher_texte(self):
        """
        Afficher la barre et le texte correspondant
        """
        # Gestion des erreurs
        if (self.err == True) and (time.time() - self.err_temps >= 5):  # Si 5 secondes se sont écoulées depuis l'erreur, on remet le dernier message valide
            self.err = False
            self.changer_texte(self.der_pas_err)

        # Barre et contour
        self.surface_barre.fill((255,255,255,0))                                                                        # Transparence
        pygame.draw.rect(self.surface_barre, self.COULEUR_CONTOUR, [0, 0, self.LONGUEUR_BARRE, self.HAUTEUR_BARRE], 3)  # Création du contour
        self.surface.blit(self.surface_barre, self.POSITION)

        # Texte
        texte = self.police_obj.render(self.chaine, True, self.COULEUR_TEXTE)
        rect_texte = texte.get_rect(center=(self.LONGUEUR_BARRE/2, self.HAUTEUR_BARRE/2))
        self.surface_barre.blit(texte, rect_texte)
        self.surface.blit(self.surface_barre, self.POSITION)