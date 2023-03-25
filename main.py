import tkinter as tk
from random import randint
#importation de pygame, et installation du module si il n'est pas déjà installé
import subprocess
import sys
try :
    import pygame
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'])
    import pygame


class PygameWindow(pygame.Surface):
    def __init__(self, size):
        super().__init__(size) #sert à éviter un problème d'héritage de classe
        pygame.init()
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption("Risk - Game")

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill((randint(0,255), randint(0,255), randint(0,255)))

            # update the window
            pygame.display.update()
#Menu principal
class MainMenue :

    def __init__(self):
        self.racine = tk.Tk()
        self.racine.attributes('-fullscreen', True)
        self.racine.title("Risk launcher")
        self.label = tk.Label(self.racine, text='REMPLISSEZ MOI CETTE FENETRE BANDE DE FAIGNASSE')
        self.label.pack()
        self.creer_widgets(self.racine)

    def creer_widgets(self, root):
        self.launch_button = tk.Button(root, text="Lancer la fenetre pygame")
        self.launch_button.bind('<Button 1>', self.pygame_launcher)
        self.launch_button.pack()

    def pygame_launcher(self, event):
        if __name__ == '__main__':
            # create the window
            window_pg = PygameWindow((640, 480))

            # run the main loop
            window_pg.main_loop()
            pygame.quit()



if __name__ == "__main__":
    app_tk = MainMenue()
    app_tk.racine.mainloop()
