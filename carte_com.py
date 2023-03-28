import pygame
from pygame.locals import *
import glob

# Set the path to the directory containing images of countries
PATH_MAP='Pictures/Maps/'

# Set the screen size
f_w=1280
f_h=800

# Define a class for representing countries as sprites
class SpritePays():
    def __init__(self,surface,name_id):
        # The surface containing the image of the country
        self.map_pays=surface
        # The id of the country (extracted from the file name)
        self.id=int(name_id[-6:-4])
        self.bounds=surface.get_bounding_rect()

# Define a function for changing the color of all non-black pixels in a surface
def color_surface(sprite,color,alpha):
	# Loop over all pixels in the surface
	for x in range(0,sprite.bounds.width):
		for y in range(0,sprite.bounds.height):
			# If the pixel is not black
			if sprite.map_pays.get_at((sprite.bounds.x+x,sprite.bounds.y+y))!=(0,0,0):
				# Change its color to the specified color
				sprite.map_pays.set_at((sprite.bounds.x+x,sprite.bounds.y+y),color)
				# Set the alpha value of the surface to the specified alpha value
				sprite.map_pays.set_alpha(alpha)


# Define a class for representing the current window
class CurrentWindow():
	def __init__(self,fenetre):
		# The Pygame window surface
		self.fenetre=fenetre
		# A list of surfaces to be displayed on top of the window surface
		self.surfaces=[]

	def afficher(self,fonction=None):
		afficher=1
		glob_pays=glob.glob(PATH_MAP+"*.png")
		sprites_pays=[]
		sprites_pays_masque=[]
		
		# Load images of countries and create SpritePays objects
		for idx,fl in enumerate(glob_pays):
			s=pygame.image.load(fl).convert()
			coeff=f_w/s.get_width()
			s=pygame.transform.scale(s,(int(coeff*s.get_width()),int(coeff*s.get_height())))
			sp=SpritePays(s,fl)
			sp_masque=SpritePays(s.copy(),fl)
			color_surface(sp_masque,(1,1,1),150)
			sprites_pays.append(sp)
			sprites_pays_masque.append(sp_masque)

        # Merge all country surfaces into a single surface
		for idx, spr in enumerate(sprites_pays):
			if idx==0:
				merged_pays = spr.map_pays.copy()
			else:
				merged_pays.blit(spr.map_pays, (0, 0))

        # Enter a loop that continues until the user quits
		while afficher:
            # Handle Pygame events
			for event in pygame.event.get():
				if event.type == QUIT:
					afficher=0

            # Blit surfaces onto the window surface
			for surface in self.surfaces:
				self.fenetre.blit(surface[0],surface[1])
            # Blit the merged country surface onto the window surface
			self.fenetre.blit(merged_pays,(0,0))
            # Update the display
			pygame.display.flip()


if __name__ == '__main__':
	pygame.init()
	fenetre = pygame.display.set_mode((f_w, f_h))
	Win=CurrentWindow(fenetre)
	Win.afficher()
