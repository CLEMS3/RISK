import tkinter as tk
from random import randint
import tkinter.font
from tkinter.scrolledtext import ScrolledText
#importation de pygame, et installation du module si il n'est pas déjà installé
import subprocess
import sys
try :
    import pygame
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'])
    import pygame
#importation de PIL
try :
    from PIL import Image,ImageTk
except :
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pillow'])
    from PIL import Image, ImageTk


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
        self.root = tk.Tk()
        self.root.title("RISK")
        self.WIDTH = self.root.winfo_screenwidth()
        self.HEIGHT = self.root.winfo_screenheight()
        self.root.geometry('%dx%d' % (self.WIDTH, self.HEIGHT))
        self.root.configure(bg='grey')

        self.root.attributes('-fullscreen', True)  # fullscreen
        # self.root.state('zoomed')      #maximised

        # import images et texts
        self.img = ImageTk.PhotoImage(file="Images\Logo_Risk.png")
        with open("Fichiers\Regles.txt", 'r') as f1:
            self.textrules = f1.read()

            # Police ecriture
        self.Impact25 = tkinter.font.Font(family='Impact', size=25)
        self.Impact15 = tkinter.font.Font(family='Impact', size=15)
        # placement des widgets
        self.create_widgets()

        self.root.bind("<Escape>", self.escape)

    def create_widgets(self):
        # Logo principal
        w = self.img.width()
        h = self.img.height()
        self.logo = tk.Canvas(self.root, width=w, height=h, bg='grey', highlightthickness=0)
        self.logo.create_image(w / 2, h / 2, image=self.img)
        self.logo.pack(pady=50)
        # Init boutons
        self.boutons_menu()

    def boutons_menu(self):
        # New game
        self.NG = tk.Button(self.root, text="NOUVELLE PARTIE", bg='grey', font=self.Impact25)
        self.NG.bind('<Button-1>', self.new_game)
        self.NG.pack(pady=80)
        # Rules
        self.rules = tk.Button(self.root, text='RÈGLES DU JEU', font=self.Impact25, bg='grey')
        self.rules.bind("<Button-1>", self.Rules_info)
        self.rules.pack(pady=30)

    def new_game(self, event):
        '''Nouveaux boutons pour choisir le nombre de joueur et lancer la partie'''
        # remove old buttons
        self.NG.destroy()
        self.rules.destroy()
        # label et scale pour choix
        self.LabelJoueur = tk.Label(self.root, text='NOMBRE DE JOUEURS', font=self.Impact25, bg="grey")
        self.LabelJoueur.pack(pady=50)
        self.NbrJoueur = tk.DoubleVar()
        self.ChoixJoueur = tk.Scale(self.root, orient='horizontal', from_=2, to=6, resolution=1, tickinterval=1,
                                    length=400, variable=self.NbrJoueur, font=self.Impact25, bg='grey',
                                    activebackground='grey', highlightbackground='grey', showvalue=False,
                                    troughcolor='red', width=20)
        self.ChoixJoueur.pack(pady=40)
        self.startlogin = tk.Button(self.root, text='VALIDER', font=self.Impact25, bg='grey')
        # bouton valider
        self.startlogin.bind("<Button-1>", self.STARTLOGIN)
        self.startlogin.pack(pady=30)
        # bouton retour
        self.BackTitle = tk.Button(self.root, text='RETOUR AU MENU', font=self.Impact15, bg='grey')
        self.BackTitle.bind("<Button-1>", self.backmenu)
        self.BackTitle.pack(pady=20)

    def backmenu(self, event):
        '''retour au menu, affichages de boutons "menu"'''
        # remove all buttons + remmettre anciens
        self.LabelJoueur.destroy()
        self.NbrJoueur = 0
        self.ChoixJoueur.destroy()
        self.BackTitle.destroy()
        self.startlogin.destroy()
        self.boutons_menu()

    def escape(self, event):
        self.root.quit()

    def escapeTOP(self, event):
        self.ruleswin.destroy()

    def Rules_info(self, event):
        """fenetre d'affichage des regles apres lecture fichier txt contenant les regles"""
        self.ruleswin = tk.Toplevel()
        self.ruleswin.title("RÈGLES DU JEU")
        self.ruleswin.attributes('-fullscreen', True)  # plein écran
        self.ruleswin.configure(bg='grey')
        self.txt1 = tk.Label(self.ruleswin, text="RÈGLES DU JEU", font=self.Impact25, bg='grey')
        self.txt1.pack(pady=50)
        self.display = ScrolledText(self.ruleswin, font=self.Impact15, width=63, bg='lightgrey')  # zone de texte
        self.display.insert(tk.INSERT, self.textrules)
        self.display.configure(state=tk.DISABLED)  # desactive l'édition
        self.display.pack()
        self.leave = tk.Button(self.ruleswin, text="J'AI COMPRIS!", font=self.Impact15, bg='grey')
        self.leave.bind("<Button-1>", self.escapeTOP)
        self.leave.pack(pady=40)

    def STARTLOGIN(self, event):
        """test"""
        print(f"login {int(self.NbrJoueur.get())} acounts")

    def pygame_launcher(self, event):
        if __name__ == '__main__':
            # create the window
            window_pg = PygameWindow((640, 480))

            # run the main loop
            window_pg.main_loop()
            pygame.quit()



if __name__ == "__main__":
    app_tk = MainMenue()
    app_tk.root.mainloop()
