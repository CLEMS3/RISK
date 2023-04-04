import tkinter as tk
from tkinter import ttk
import csv
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
class MainMenu :

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RISK")
        self.WIDTH = self.root.winfo_screenwidth()
        self.HEIGHT = self.root.winfo_screenheight()
        self.root.geometry('%dx%d' % (self.WIDTH, self.HEIGHT))
        self.root.configure(bg='grey')

        self.root.attributes('-fullscreen', True)  # fullscreen
        # self.root.state('zoomed')      #maximised

        # imports
        self.img = tk.PhotoImage(file='Images/Logo_Risk.png')



        
        with open("Fichiers/Regles.txt", 'r') as f1:
            self.textrules = f1.read()
        #joueurs
        with open('Joueurs.csv', 'r' ) as f2:
            csv_joueur = csv.reader(f2,delimiter=";")
            csv_joueur.__next__()
            self.liste_joueurs = []
            for row in csv_joueur:
                PLAYER = Joueur(row[0],row[1],row[2],row[3])
                self.liste_joueurs.append(PLAYER)
                #print(self.liste_joueurs)

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
        self.NG = tk.Button(self.root, text="NOUVELLE PARTIE", bg='grey', font=self.Impact25,command = self.new_game)
        #self.NG.bind('<Button-1>', self.new_game)
        self.NG.pack(pady=80)
        # Rules
        self.rules = tk.Button(self.root, text='RÈGLES DU JEU', font=self.Impact25, bg='grey', command = self.Rules_info)
    
        self.rules.pack(pady=30)

    def new_game(self):
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
        # bouton valider
        self.startlogin = tk.Button(self.root, text='Valider', font=self.Impact25, bg='grey', command = self.STARTLOGIN)
        self.startlogin.pack(pady=30)
        # bouton retour
        self.BackTitle = tk.Button(self.root, text='Retour', font=self.Impact15, bg='grey',command = self.backmenu)
        self.BackTitle.pack(pady=20)

    def backmenu(self):
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

    def escapeTOP(self):
        self.ruleswin.destroy()

    def Rules_info(self):
        """fenetre d'affichage des regles apres lecture fichier txt contenant les regles"""
        self.ruleswin = tk.Toplevel()
        self.ruleswin.title("Règles du jeu")
        self.ruleswin.attributes('-fullscreen', True)  # plein écran
        self.ruleswin.configure(bg='grey')
        self.txt1 = tk.Label(self.ruleswin, text="Règles du jeu", font=self.Impact25, bg='grey')
        self.txt1.pack(pady=50)
        self.display = ScrolledText(self.ruleswin, font=self.Impact15, width=63, bg='lightgrey')  # zone de texte
        self.display.insert(tk.INSERT, self.textrules)
        self.display.configure(state=tk.DISABLED)  # desactive l'édition
        self.display.pack()
        self.leave = tk.Button(self.ruleswin, text="J'ai compris!", font=self.Impact15, bg='grey', command = self.escapeTOP)
        self.leave.pack(pady=40)

    def STARTLOGIN(self):
        """test"""
        print(f"login {int(self.NbrJoueur.get())} acounts")
        #menage, on enleve les anciens widgets
        self.LabelJoueur.destroy()
        self.ChoixJoueur.destroy()
        self.BackTitle.destroy()
        self.startlogin.destroy()
        #nombre de comptes à connecter
        self.test = tk.Label(self.root, text =f'{int(self.NbrJoueur.get())} comptes à connecter', font = self.Impact25, bg='grey')
        self.test.pack()
        self.box = tk.Frame(bg='grey', width= 100)
        self.box.pack(pady=50)
        #rangée de boutons pour chaque connection
        self.buttonPlayer = []
        for i in range(int(self.NbrJoueur.get())):
            self.buttonPlayer.append(tk.Button(self.box, text='Joueur '+str(i+1),bg='grey', font = self.Impact25,command=lambda i=i: self.login_win(i)))
            self.buttonPlayer[i].grid(column=i, row=0, sticky=tk.W)
        #creer un compte
        self.create_acc = tk.Button(self.root, text = 'Créer un compte', bg = 'grey', font = self.Impact15) ##PAS ENCORE DE COMMANDE 
        self.create_acc.pack(pady=30)
        self.back_button = tk.Button(self.root, text = 'Retour', font = self.Impact15, bg='grey', command = self.back)
        self.back_button.pack(pady=10)

    def login_win(self,i):
        '''fenetre TOPlayer pour se connecter ou creer un compte'''
     
        self.login_page = tk.Toplevel()
        self.login_page.attributes('-fullscreen', True)  # plein écran
        self.login_page.configure(bg='grey')
        self.Textbox = tk.Label(self.login_page, text =f'Joueur {i+1}', font = self.Impact25, bg='grey')
        self.Textbox.pack(pady=100)
        #choix du joueur
        self.choix_joueur = ttk.Combobox(self.login_page, values = ['Selectionnez un joueur'] + self.liste_joueurs, font = self.Impact25, state="readonly", background='grey')
        self.choix_joueur.current(0)
        self.choix_joueur.pack()
        #mot de passe
        self.label2 = tk.Label(self.login_page, text = 'Mot de Passe', font = self.Impact25, bg='grey')
        self.label2.pack(pady=50)
        self.mdpentry = tk.Entry(self.login_page,show="*", font = self.Impact25)
        self.mdpentry.pack()
        self.validation = tk.Button(self.login_page, text = 'Valider', command = lambda :self.checkmdp(i,self.choix_joueur.get()), font = self.Impact25, bg='grey')
        self.validation.pack(pady=30)
        #self.login_page.bind('<Enter>', self.checkmdp(self.numero_joueur))
        #bouton retour
        self.retour = tk.Button(self.login_page, text = 'Retour', command = lambda :self.login_page.destroy(), font = self.Impact15, bg='grey')
        self.retour.pack(pady=10)
    
    def checkmdp(self,i,joueur):
        print(f'joueur {i+1},{joueur}')
        if joueur == 'Selectionnez un joueur':
            try:
                self.errorlabel.destroy()
            except:
                None 
            self.errorlabel = tk.Label(self.login_page, text = "Veuillez choisir un joueur", font = self.Impact15, fg='red', bg='grey')
            self.errorlabel.pack(pady = 10)
        else:
            try:
                self.errorlabel.destroy()
            except:
                None
        #si mdp ok, fermer top level et desactiver bouton du joueur qui a validé (mettre en vert le nom du joueur sur le bouton)



    def back(self):
        self.create_acc.destroy()
        self.test.destroy()
        self.box.destroy()
        self.back_button.destroy()
        self.new_game()

    def pygame_launcher(self):
        if __name__ == '__main__':
            # create the window
            window_pg = PygameWindow((640, 480))

            # run the main loop
            window_pg.main_loop()
            pygame.quit()
   
    
class Joueur():

    def __init__(self,ID,nom,MDP,GameWin):
        self.ID = ID
        self.nom = nom
        self.mdp = MDP
        self.win = GameWin

    #def __str__(self):
        #return(f'le nom du joueur {str(self.ID)} est {str(self.nom)}, il a gangé {str(self.win)} parties')
        
    def __repr__(self):
        return(f'{str(self.nom)}')



if __name__ == "__main__":
    app_tk = MainMenu()
    app_tk.root.mainloop()