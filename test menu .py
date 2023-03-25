
### test menu ###

import tkinter as tk
from PIL import Image,ImageTk
import tkinter.font 
from tkinter.scrolledtext import ScrolledText


class menu():

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("RISK")
        self.WIDTH = self.root.winfo_screenwidth()
        self.HEIGHT = self.root.winfo_screenheight()
        self.root.geometry('%dx%d'%(self.WIDTH,self.HEIGHT))
        self.root.configure(bg = 'grey')

        self.root.attributes('-fullscreen', True) #fullscreen
        #self.root.state('zoomed')      #maximised

        #import images et texts
        self.img= ImageTk.PhotoImage(file ="Images\Logo_Risk.png")
        with open("Fichiers\Regles.txt",'r') as f1:
            self.textrules = f1.read()  
         
    
        #Police ecriture
        self.Impact25 = tkinter.font.Font(family='Impact', size = 25)
        self.Impact15 = tkinter.font.Font(family='Impact', size = 15)
        #placement des widgets
        self.create_widgets()
        
        
        self.root.bind("<Escape>", self.escape)


    def create_widgets(self):
        #Logo principal
        w = self.img.width()
        h = self.img.height()
        self.logo = tk.Canvas(self.root, width = w, height= h, bg='grey',highlightthickness=0)
        self.logo.create_image(w/2,h/2,image=self.img)
        self.logo.pack(pady = 50)
        #Init boutons
        self.boutons_menu() 


    def boutons_menu(self):
        #New game
        self.NG = tk.Button(self.root, text = "NOUVELLE PARTIE", bg= 'grey', font = self.Impact25 )
        self.NG.bind('<Button-1>',self.new_game)
        self.NG.pack(pady=80)
        #Rules
        self.rules = tk.Button(self.root, text = 'RÈGLES DU JEU', font =self.Impact25, bg = 'grey')
        self.rules.bind("<Button-1>", self.Rules_info)
        self.rules.pack(pady=30)

    def new_game(self,event):
        self.NG.destroy()
        self.rules.destroy()
        self.LabelJoueur = tk.Label(self.root, text='NOMBRE DE JOUEURS', font = self.Impact25, bg="grey")
        self.LabelJoueur.pack(pady=50)
        self.NbrJoueur = tk.DoubleVar()
        self.ChoixJoueur = tk.Scale(self.root, orient='horizontal', from_=2, to=6,resolution=1, tickinterval=1,length=400, variable = self.NbrJoueur, font=self.Impact25, bg='grey', activebackground ='grey', highlightbackground='grey', showvalue = False, troughcolor='red', width = 20)
        self.ChoixJoueur.pack(pady=40)
        self.startlogin = tk.Button(self.root, text = 'VALIDER', font = self.Impact25, bg = 'grey')
        self.startlogin.bind("<Button-1>", self.STARTLOGIN)
        self.startlogin.pack(pady=30)
        self.BackTitle = tk.Button(self.root, text = 'RETOUR AU MENU', font = self.Impact15, bg = 'grey')
        self.BackTitle.bind("<Button-1>", self.backmenu)
        self.BackTitle.pack(pady=20)

    def backmenu(self,event):
        self.LabelJoueur.destroy()
        self.NbrJoueur=0
        self.ChoixJoueur.destroy()
        self.BackTitle.destroy()
        self.startlogin.destroy()
        self.boutons_menu()
    

    def escape(self,event):
        self.root.quit()
    
    def escapeTOP(self,event):
        self.ruleswin.destroy()

    def Rules_info(self, event):
        self.ruleswin = tk.Toplevel()
        self.ruleswin.title("RÈGLES DU JEU")
        #self.ruleswin.geometry('%dx%d'%(self.WIDTH,self.HEIGHT))
        self.ruleswin.attributes('-fullscreen', True)
        self.ruleswin.configure(bg = 'grey')
        self.txt1 = tk.Label(self.ruleswin, text = "RÈGLES DU JEU", font = self.Impact25, bg='grey')
        self.txt1.pack(pady=50)
        self.ruleswin.update()
        self.display = ScrolledText(self.ruleswin, font=self.Impact15,width =63, bg='lightgrey')
        self.display.insert(tk.INSERT, self.textrules)
        self.display.configure(state = tk.DISABLED)
        self.display.pack()
        self.leave = tk.Button(self.ruleswin, text = "J'AI COMPRIS!",font = self.Impact15, bg='grey')
        self.leave.bind("<Button-1>", self.escapeTOP)
        self.leave.pack(pady=40)

    def STARTLOGIN(self,event):
        print(f"login {int(self.NbrJoueur.get())} acounts")











test = menu()
test.root.mainloop()
#test
