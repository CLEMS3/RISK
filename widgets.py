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
                    self.increment()
                else:
                    self.decrement()