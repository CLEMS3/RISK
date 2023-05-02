import tkinter as tk
from tkinter import ttk
import csv
import time
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
import hashlib
import carte_final

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
        with open('Fichiers/Joueurs.csv', 'r', encoding='windows-1252' ) as f2:
            csv_joueur = csv.reader(f2,delimiter=",")
            csv_joueur.__next__()
            self.liste_joueurs = []
            self.liste_pseudo = []
            
            for row in csv_joueur:
                PLAYER = Joueur(row[0],row[1],row[2])
                self.liste_joueurs.append(PLAYER) #liste des joueur (class)
                self.liste_pseudo.append(row[1]) #liste des pseudo (pour eviter les doublons)
                
            f2.close()
        self.loged_in = []
        self.OUT = [] #liste des joueurs connecté lors du lancement de la partie, sert pour init le jeu
        

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
        self.logo.pack(pady=80)
        # Init boutons
        self.boutons_menu()

    def boutons_menu(self):
        # New game
        self.NG = tk.Button(self.root, text="NOUVELLE PARTIE", bg='grey', font=self.Impact25,command = self.new_game)
        #self.NG.bind('<Button-1>', self.new_game)
        self.NG.pack(pady=30)
        #classement des joueurs
        self.classement = tk.Button(self.root, text='CLASSEMENT', bg='grey', font=self.Impact25, command=self.classwin)
        self.classement.pack(pady=30)
        # Rules
        self.rules = tk.Button(self.root, text='RÈGLES DU JEU', font=self.Impact25, bg='grey', command = self.Rules_info)
        self.rules.pack(pady=30)

    def new_game(self):
        '''Nouveaux boutons pour choisir le nombre de joueur et lancer la partie'''
        # remove old buttons
        self.classement.destroy()
        self.NG.destroy()
        self.rules.destroy()
        # label et scale pour choix
        self.LabelJoueur = tk.Label(self.root, text='NOMBRE DE JOUEURS', font=self.Impact25, bg="grey")
        self.LabelJoueur.pack(pady=40)
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

    def liste_play_classe(self):
        test= []
        for player in self.liste_joueurs:
            test.append(player.win)
        test.sort(reverse=True)
        self.liste_classe=[]
        tempo = list(self.liste_joueurs)
        print(test)
        try:
            for i in range(5):
                for player in tempo:
                    if player.win == test[i]:
                        self.liste_classe.append(player)
                        tempo.remove(player)
        except:
            for i in range(len(tempo)):
                for player in tempo:
                    if player.win == test[i]:
                        self.liste_classe.append(player)
                        tempo.remove(player)
        

    def backmenu(self):
        '''retour au menu apres avoir cliqué sur'NOUVELLE PARTIE', affichages de boutons "menu"'''
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

    def escapeTOP2(self):
        self.TOP2.destroy()

    def playerbutton_enter(self,event,i):
        self.playername[i].config(text=self.liste_classe[i].win+"  victoires")

    def playerbutton_leave(self,event,i):
        self.playername[i].config(text=self.liste_classe[i].nom)        


    def classwin(self):
        self.TOP2 = tk.Toplevel()
        self.TOP2.title("Classement")
        self.TOP2.attributes('-fullscreen', True)  # plein écran
        self.TOP2.configure(bg='grey')
        self.txt2 = tk.Label(self.TOP2, text="Classement des joueurs \n\n TOP 5", font=self.Impact25, bg='grey')
        self.txt2.pack(pady=50)
        self.zone = tk.Frame(self.TOP2,bg='grey')
        self.zone.pack(pady=30)
        self.liste_play_classe()
        self.playername = []
        for i in range(len(self.liste_classe)):
            self.playername.append(tk.Button(self.zone, text=self.liste_classe[i].nom ,bg='lightgray', font = self.Impact25))
            self.playername[i].bind('<Enter>',lambda event, i=i : self.playerbutton_enter(event, i))
            self.playername[i].bind('<Leave>',lambda event, i=i : self.playerbutton_leave(event, i))
            self.playername[i].grid(column=0, row=i, sticky=tk.N)
        self.back3 = tk.Button(self.TOP2, text= 'Retour', font=self.Impact15, bg='grey', command=self.escapeTOP2 )
        self.back3.pack(pady=30)
            

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
        '''fenetre pour boutons de connection et creation de compte'''
        print(f"login {int(self.NbrJoueur.get())} acounts")
        #menage, on enleve les anciens widgets
       
        self.LabelJoueur.destroy()
        self.ChoixJoueur.destroy()
        self.BackTitle.destroy()
        self.startlogin.destroy()
        #nombre de comptes à connecter
        self.text = tk.Label(self.root, text =f'{int(self.NbrJoueur.get())} comptes à connecter', font = self.Impact25, bg='grey')
        self.text.pack()
        self.box = tk.Frame(bg='grey', width= 100)
        self.box.pack(pady=30)
        #rangée de boutons pour chaque connection
        self.buttonPlayer = []
        for i in range(int(self.NbrJoueur.get())):
            self.buttonPlayer.append(tk.Button(self.box, text='Joueur '+str(i+1),bg='grey', font = self.Impact25,command=lambda i=i: self.login_win(i)))
            self.buttonPlayer[i].grid(column=i, row=0, sticky=tk.W)
        #Valider
        self.launch_game = tk.Button(self.root, text= 'Lancer la partie', bg='grey',fg='orange' ,activebackground='orange', activeforeground='black', font=self.Impact25, command = self.pygame_launcher)
        self.launch_game.pack(pady=20)
        #creer un compte
        self.create_acc = tk.Button(self.root, text = 'Créer un compte', bg = 'grey', font = self.Impact15, command = self.NewAccount)
        self.create_acc.pack(pady=20)
       
        #Bouton Retour
        self.back_button = tk.Button(self.root, text = 'Retour', font = self.Impact15, bg='grey', command = self.back)
        self.back_button_ttp = CreateToolTip(self.back_button, "Attention, tous les comptes seront déconnectés si vous quittez cette fenêtre")
        self.back_button.pack(pady=10)

    def login_win(self,i):
        '''fenetre TOPlayer pour se connecter'''
     
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
        
        #bouton retour
        self.retour = tk.Button(self.login_page, text = 'Retour',command =lambda : self.login_page.destroy()  , font = self.Impact15, bg='grey')
        self.retour.pack(pady=10)
    
    def checkmdp(self,i,joueur):
        '''verifie le mot de passe et valide la connection'''
        print(f'joueur {i+1},{joueur}')

        ok = 0 #joueur selectionné ou pas

        #enleve les label d'erreur si il y'en a
        try: self.errorlabel4.destroy()
        except:
            None

        try: self.errorlabel3.destroy()
        except:
            None

        if joueur == 'Selectionnez un joueur': #verifie qu'un joueur à été selectionné
            try: 
                self.errorlabel.destroy()
            except: None 
            self.errorlabel = tk.Label(self.login_page, text = "Veuillez choisir un joueur", font = self.Impact15, fg='red', bg='grey')
            self.errorlabel.pack(pady = 20)
        elif joueur in self.loged_in: #verifie que le joueur n'est pas déjà connecté
            try: self.errorlabel.destroy()
            except: None
            self.errorlabel4 = tk.Label(self.login_page, text = "Joueur déja connecté", font = self.Impact15, fg='red', bg='grey')
            self.errorlabel4.pack(pady = 20)
        else:
            try: self.errorlabel.destroy()
            except: None
            ok = 1
        mdpTRY = self.mdpentry.get() #récupère le mdp inséré
        mdpHashed =  hashlib.sha256(mdpTRY.encode('UTF-8')).hexdigest() #encode le mdp

        
        if ok == 1:
            for player in self.liste_joueurs:
                if player.nom == joueur: #choisis le bon joueur
                
                    if player.mdp == mdpHashed: #verifie le mot de passe
                        self.login_page.destroy()
                        self.buttonPlayer[i].configure(bg='green',fg='black')
                        self.buttonPlayer[i]['state']='disabled'
                        self.loged_in.append(joueur)
                        self.OUT.append(player)
                        print(self.loged_in)

                    else:
                        
                        self.mdpentry.delete(0,'end')
                        self.errorlabel3 = tk.Label(self.login_page, text = 'Mauvais Mot De Passe', font=self.Impact15, bg='grey', fg='red')
                        self.errorlabel3.pack(pady=20)

    def back(self):
        self.create_acc.destroy()
        self.text.destroy()
        self.box.destroy()
        self.back_button.destroy()
        self.launch_game.destroy()
        self.new_game()
        self.loged_in = []     
        self.OUT = []   

    def pygame_launcher(self):
        if __name__ == '__main__':
            print(int(self.NbrJoueur.get()))
            print(self.OUT)
            if len(self.OUT) == int(self.NbrJoueur.get()):
                # create the window
                window_pg = carte_final.PygameWindow((self.WIDTH, self.HEIGHT), self.liste_joueurs)

                # run the main loop
                window_pg.main_loop()
                pygame.quit()
          
    def NewAccount(self):
        '''Fenetre creation de compte'''
        self.TL = tk.Toplevel()
        self.TL.attributes('-fullscreen', True)  # plein écran
        self.TL.configure(bg='grey')
        self.Textbox2 = tk.Label(self.TL, text ='Nouveau Compte', font = self.Impact25, bg='grey')
        self.Textbox2.pack(pady=60)
        self.NameLabel = tk.Label(self.TL, text ='Choisir un pseudo', font = self.Impact25, bg='grey')
        self.NameLabel.pack(pady=20)
        self.Name = tk.Entry(self.TL, font = self.Impact25)
        self.Name.pack(pady=30)
        self.MdpLabel1 = tk.Label(self.TL, text ='Choisir un Mot De Passe', font = self.Impact25, bg='grey')
        self.MdpLabel1.pack(pady=30)
        self.Mdp = tk.Entry(self.TL, font = self.Impact25, show = '*')
        self.Mdp.pack(pady=20)
        self.Validate = tk.Button(self.TL, text = 'Valider', font = self.Impact25,bg='grey', command = self.addplayer)
        self.Validate.pack(pady=30)
        self.back2 = tk.Button(self.TL, text='Retour', font = self.Impact15, bg='grey', command = lambda : self.TL.destroy())
        self.back2.pack(pady=20)

    def addplayer(self):
        '''Ajoute un compte joueur dans le fichier csv + dans la liste du /main'''
        name= self.Name.get()
        password = self.Mdp.get()
        
        try:
            self.errorlabel2.destroy() 
        except: None
        try:
            self.errorlabel6.destroy() 
        except: None

        if name not in self.liste_pseudo and len(name) >= 1:
            if len(password) > 5 :
                hashed_mdp = hashlib.sha256(password.encode('UTF-8')).hexdigest() #encode le mot de passe pour le stockage
                with open('Fichiers/Joueurs.csv', 'a', newline='') as f3:
                    writer = csv.writer(f3)
                    nouvelles_données = [name,hashed_mdp,0]
                    self.liste_joueurs.append(Joueur(name,hashed_mdp,0))
                    self.liste_pseudo.append(name)
                    writer.writerow(nouvelles_données)
                    f3.close()
                    self.TL.destroy()
            else:
                self.errorlabel6 = tk.Label(self.TL, text = "Votre mot de passe doit être plus long", font = self.Impact15, fg='red', bg='grey')
                self.errorlabel6.pack(pady=10)
                            
        else:
            self.errorlabel2 = tk.Label(self.TL, text = "Pseudo non conforme", font = self.Impact15, fg='red', bg='grey')
            self.errorlabel2.pack(pady=10)
    
    

class Joueur():

    def __init__(self,nom,MDP,GameWin):

        self.nom = nom
        self.mdp = MDP
        self.win = GameWin

    #def __str__(self):
        #return(f'le nom du joueur {str(self.ID)} est {str(self.nom)}, il a gangé {str(self.win)} parties')
        
    def __repr__(self):
        return(f'{str(self.nom)}')

class CreateToolTip(object): #par crxguy52 sur Stackoverflow 25/03/2016
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="grey",fg='red', relief='solid', borderwidth=1,
                       wraplength = self.wraplength, font= tkinter.font.Font(family='Impact', size=15) )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()    

if __name__ == "__main__":
    app_tk = MainMenu()
    app_tk.root.mainloop()