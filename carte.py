###################
###### BLOB #######
###################

import pygame
from pygame.locals import *
import glob


PATH_MAP='Pictures/Maps/'
f_w=1280
f_h=800



###################
###### CODE #######
###################

class SpritePays():
    def __init__(self,surface,name_id):
        self.map_pays=surface
        self.name_pays=''
        self.id=int(name_id[-6:-4])#pas tres propre
        self.bounds=surface.get_bounding_rect()


def color_surface(sprite,color,alpha):
    """
    Bing :
    
    The `color_surface` function takes a `SpritePays` object, a color, and an alpha value as arguments. The function changes the color of all non-black pixels in the `map_pays` surface of the `SpritePays` object to the specified color. The alpha value of the surface is also set to the specified alpha value.

    This function is used in the code to create a semi-transparent white mask for each country by calling `color_surface(sp_masque,(1,1,1),150)` on a copy of each country's surface. This mask is used to highlight countries when the user hovers their mouse over them.

    In summary, the `color_surface` function changes the color of all non-black pixels in a surface and sets its alpha value.
    """
    for x in range(0,sprite.bounds.width):
        for y in range(0,sprite.bounds.height):
            if sprite.map_pays.get_at((sprite.bounds.x+x,sprite.bounds.y+y))!=(0,0,0):
                sprite.map_pays.set_at((sprite.bounds.x+x,sprite.bounds.y+y),color)
                sprite.map_pays.set_alpha(alpha)

class CurrentWindow():

    def __init__(self,fenetre):
        self.fenetre=fenetre
        self.surfaces = []



    def afficher(self,fonction=None):
        afficher=1
        glob_pays=glob.glob(PATH_MAP+"*.png")
        sprites_pays=[]
        #sprites de passage
        sprites_pays_masque=[]
        #chagement des sprites de pays
        for idx,fl in enumerate(glob_pays):
            s=pygame.image.load(fl).convert()
            coeff=f_w/s.get_width()
            s=pygame.transform.scale(s,(int(coeff*s.get_width()),int(coeff*s.get_height())))
            sp=SpritePays(s,fl)
            sp_masque=SpritePays(s.copy(),fl)
            color_surface(sp_masque,(1,1,1),150)
            sprites_pays.append(sp)
            sprites_pays_masque.append(sp_masque)

        #colorisation des pays selon les couleurs des joueurs
        # self.color_players(sprites_pays)
        for idx, spr in enumerate(sprites_pays):#pas super propre
            if idx==0:
                merged_pays = spr.map_pays.copy()
            else:
                merged_pays.blit(spr.map_pays, (0, 0))

        #affichage des troupes
        while afficher:
            for event in pygame.event.get():
                if event.type == QUIT:
                    afficher=0


            for surface in self.surfaces:
                self.fenetre.blit(surface[0],surface[1])
            self.fenetre.blit(merged_pays,(0,0))
            pygame.display.flip()


	# def start_game(self):
	# 	self.surfaces=[]

	# 	#map
	# 	map_monde=pygame.image.load(PATH_IMG+MAP_IMG).convert_alpha()
	# 	coeff=f_w/map_monde.get_width()#adapte l'image selon la largeur
	# 	w=int(coeff*map_monde.get_width())
	# 	h=int(coeff*map_monde.get_height())
	# 	map_monde=pygame.transform.scale(map_monde,(w,h))


if __name__ == '__main__':

	pygame.init()
	fenetre = pygame.display.set_mode((f_w, f_h))
	Win=CurrentWindow(fenetre)
	# Win.fonctions.append(Win.start_game)		#fonctions ini 

	Win.afficher()	#on rentre dans la boucle while d'affichage