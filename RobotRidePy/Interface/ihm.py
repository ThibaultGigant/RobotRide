from tkinter.filedialog import *
from tkinter.messagebox import *
from Robot.file_gestion import *
import os


apropos_message = """Ce programme est un projet réalisé par Thibault Gigant pour le projet de MOGPL en 2015
Le but de ce programme est de trouver le chemin le plus rapide d'un robot dans un entrepôt entre deux points"""


class TopMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.menu_fichier()
        self.menu_aide()
        self.parent.config(menu=self)

    def menu_fichier(self):
        menu1 = Menu(self, tearoff=0)
        menu1.add_command(label="Ouvrir", command=self.parent.lancer_fichier)
        # menu1.add_command(label="Créer", command=self.parent.lancer_base)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.parent.quit)
        self.add_cascade(label="Fichier", menu=menu1)

    def menu_aide(self):
        menu2 = Menu(self, tearoff=0)
        menu2.add_command(label="A propos", command=apropos)
        self.add_cascade(label="Aide", menu=menu2)


class RightFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.opened_widgets = []

    def clean(self):
        for i in self.opened_widgets:
            i.destroy()

    def choice_buttons(self):
        self.clean()
        open_button = Button(self.parent, text="Récupérer un problème depuis un fichier",
                             command=self.parent.lancer_fichier)
        create_button = Button(self.parent, text="Créer manuellement un problème",
                               command=self.parent.lancer_fichier)
        open_button.grid(column=0, row=0)
        create_button.grid(column=0, row=1)
        self.opened_widgets.append(open_button)
        self.opened_widgets.append(create_button)

    def demander_sortie(self):
        self.clean()
        label = Label(self, text="Fichier d'entrée")
        entry = Entry(self, textvariable=self.parent.entree)
        bouton = Button(self, text="Changer le fichier d'entrée", command=self.parent.lancer_fichier)
        label.grid(column=0, row=0, columnspan=3)
        entry.grid(column=0, row=1, columnspan=2)
        bouton.grid(column=2, row=1)
        self.opened_widgets.append(label)
        self.opened_widgets.append(entry)
        self.opened_widgets.append(bouton)

        # On demande enfin la sortie
        label = Label(self, text="Fichier de sortie")
        entry = Entry(self, textvariable=self.parent.sortie)
        bouton = Button(self, text="Choisir un fichier existant",
                        command=lambda: self.parent.sortie.set(choisir_fichier("Choisir un fichier de sortie")))
        label.grid(column=0, row=2, columnspan=3)
        entry.grid(column=0, row=3, columnspan=2)
        bouton.grid(column=2, row=3)
        self.opened_widgets.append(label)
        self.opened_widgets.append(entry)
        self.opened_widgets.append(bouton)

        # Lancement de l'algorithme
        validate_button = Button(self, text="Lancer l'algorithme", command=self.parent.lancer_algo)
        validate_button.grid(column=0, row=4, columnspan=3)
        self.opened_widgets.append(validate_button)


class LeftFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.opened_widgets = []
        self.initialize()

    def initialize(self):
        canvas = Canvas(self, width=800, height=700)
        for i in range(0, 800, 800//20):
            for j in range(0, 700, 700//20):
                rectangle(canvas, i, j, i+800//20, j+700//20)
        canvas.pack()
        self.opened_widgets.append(canvas)

    def afficher_resultat(self, resultat, tps_creat, tps_calc):
        for i in range(len(resultat)):
            label = Label(self, text="Problème n°"+str(i))
            label_res = Label(self, text=resultat[i])
            label_tps_creat = Label(self, text="La création du graphe a pris " + str(tps_creat[i]) + " secondes")
            label_tps_calc = Label(self, text="Le calcul de la solution a pris " + str(tps_calc[i]) + " secondes")
            label.pack()
            label_res.pack()
            label_tps_creat.pack()
            label_tps_calc.pack()
            self.opened_widgets.append(label)
            self.opened_widgets.append(label_res)
            self.opened_widgets.append(label_tps_creat)
            self.opened_widgets.append(label_tps_calc)


class FenetrePrincipale(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.entree = StringVar()
        self.sortie = StringVar()
        self.entree.set("/Users/Tigig/Documents/Travail/M1/M1-MOGPL/RobotRidePy/Instances/x9y10o10.dat")
        self.sortie.set("/Users/Tigig/Documents/Travail/M1/M1-MOGPL/RobotRidePy/Instances/Résultats/x9y10o10out.dat")
        self.menu = None
        self.leftFrame = None
        self.rightFrame = None
        self.initialize()

    def initialize(self):
        self.grid()
        self.menu = TopMenu(self)
        self.rightFrame = RightFrame(self)
        self.leftFrame = LeftFrame(self)
        self.leftFrame.pack(side=LEFT, padx=10, pady=10)
        self.rightFrame.pack(side=RIGHT, padx=10, pady=10)
        self.menu_principal()

    def menu_principal(self):
        self.choice_buttons()

    def clear_fenetre(self):
        if self.leftFrame:
            for i in self.leftFrame.opened_widgets:
                i.destroy()
        if self.rightFrame:
            for i in self.rightFrame.opened_widgets:
                i.destroy()

    def choice_buttons(self):
        self.rightFrame.choice_buttons()

    def lancer_fichier(self):
        self.rightFrame.demander_sortie()

    def lancer_algo(self):
        if os.path.isfile(self.entree.get()):
            if os.path.isfile(self.sortie.get()):
                if not askyesno("Fichier existant", "Le fichier " + self.sortie.get() + " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
                    return
            if self.sortie.get():
                resultat, tps_creat, tps_calc = lecture(self.entree.get(), self.sortie.get())
                self.leftFrame.afficher_resultat(resultat, tps_creat, tps_calc)
            else:
                showerror("Erreur Fichiers", "Le fichier de sortie est incorrect")
        else:
            showerror("Erreur Fichiers", "Le fichier d'entrée est introuvable")


# Méthodes en dehors des classes, communes
def choisir_fichier(titre):
    return askopenfilename(title=titre, filetypes=[('dat files', '*.dat'), ('all files', '.*')])


def apropos():
    showinfo("Robot Ride !", apropos_message)


def rectangle(canvas, x1, y1, x2, y2, color="#FEFF8E"):
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)


def affichage_fenetre():
    fenetre = FenetrePrincipale(None)
    fenetre.title("Robot Ride !")
    fenetre.mainloop()
