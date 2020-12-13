from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from joueur.joueur import Joueur
from plateau.plateau import Plateau
import sqlite3
import random
from datetime import date

Window.hide()

Builder.load_file("QuantikGame/interface.kv")


class MenuPrincipale(Screen):
    pass

class MenuRegles(Screen):
    pass


class MenuJouer(Screen):

    def verrouillerPlateau(self, param):
        for ligne in acces_plateau.plateau:
            for case in ligne:
                if len(case) == 2:
                    self.ids[case].disabled = param
                    self.ids[case].background_disabled_normal = "QuantikGame/imgs/jouer/cell.png"
                    self.ids[case].background_disabled_down = "QuantikGame/imgs/jouer/cell.png"

    def retourMenu(self):
        acces_plateau.plateau = [["A1","A2","A3","A4"],
                                ["B1","B2","B3","B4"],
                                ["C1","C2","C3","C4"],
                                ["D1","D2","D3","D4"]]

        self.verrouillerPlateau(False)
        self.ids["victoire"].text = ""
        self.ids["spinnerPieces"].values = ("Carré", "Rond", "Triangle", "Croix")
        acces_joueur1.pieces = {"carre":2,
                          "rond":2,
                      "triangle":2,
                         "croix":2}

        acces_joueur2.pieces = {"carre": 2,
                                "rond": 2,
                                "triangle": 2,
                                "croix": 2}

    def commencerPartie(self):
        global nb_coups
        nb_coups = 0
        nb_random = int(random.uniform(0, 2))
        if nb_random == 0:
            self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo
            acces_joueur1.couleur = "rouge"
            acces_joueur2.couleur = "bleu"
        else:
            self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            acces_joueur2.couleur = "rouge"
            acces_joueur1.couleur = "bleu"

    def mettrePiece(self, id):
        global nb_coups
        self.joueurQuiAJoue = ""

        if nb_coups%2 == 0 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur1

        elif nb_coups%2 == 0 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups%2 == 1 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups%2 == 1 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur1

        self.couleur = self.joueurQuiAJoue.couleur

        if (self.ids["spinnerPieces"].text == "Carré") and (self.joueurQuiAJoue.pieces["carre"] > 0):
            self.ids[id].disabled = True
            self.ids[id].background_disabled_normal = "QuantikGame/imgs/jouer/carre_" + self.couleur +".png"
            self.ids[id].background_disabled_down = "QuantikGame/imgs/jouer/carre_"+ self.couleur +".png"
            self.joueurQuiAJoue.pieces["carre"] -= 1
            nb_coups += 1
            self.ids["spinnerPieces"].text = "Pièces"
            self.ids["nbPieces"].text = ""
            if self.joueurQuiAJoue.pseudo == acces_joueur2.pseudo:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            else:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo

            self.mettrePieceDansPlateau("carre", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117,0.0156,0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

        elif(self.ids["spinnerPieces"].text == "Rond") and (self.joueurQuiAJoue.pieces["rond"] > 0):
            self.ids[id].disabled = True
            self.ids[id].background_disabled_normal = "QuantikGame/imgs/jouer/rond_" + self.couleur + ".png"
            self.ids[id].background_disabled_down = "QuantikGame/imgs/jouer/rond_" + self.couleur + ".png"
            self.joueurQuiAJoue.pieces["rond"] -= 1
            nb_coups += 1
            self.ids["spinnerPieces"].text = "Pièces"
            self.ids["nbPieces"].text = ""
            if self.joueurQuiAJoue == acces_joueur2:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            else:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo
            self.mettrePieceDansPlateau("rond", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))


        elif(self.ids["spinnerPieces"].text == "Triangle") and (self.joueurQuiAJoue.pieces["triangle"] > 0):
            self.ids[id].disabled = True
            self.ids[id].background_disabled_normal = "QuantikGame/imgs/jouer/triangle_" + self.couleur + ".png"
            self.ids[id].background_disabled_down = "QuantikGame/imgs/jouer/triangle_" + self.couleur + ".png"
            self.joueurQuiAJoue.pieces["triangle"] -= 1
            nb_coups += 1
            self.ids["spinnerPieces"].text = "Pièces"
            self.ids["nbPieces"].text = ""
            if self.joueurQuiAJoue == acces_joueur2:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            else:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo
            self.mettrePieceDansPlateau("triangle", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

        elif(self.ids["spinnerPieces"].text == "Croix") and (self.joueurQuiAJoue.pieces["croix"] > 0):
            self.ids[id].disabled = True
            self.ids[id].background_disabled_normal = "QuantikGame/imgs/jouer/croix_" + self.couleur + ".png"
            self.ids[id].background_disabled_down = "QuantikGame/imgs/jouer/croix_" + self.couleur + ".png"
            self.joueurQuiAJoue.pieces["croix"] -= 1
            nb_coups += 1

            self.ids["spinnerPieces"].text = "Pièces"
            self.ids["nbPieces"].text = ""
            if self.joueurQuiAJoue == acces_joueur2:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            else:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo
            self.mettrePieceDansPlateau("croix", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouillerPlateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouterDonnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

    def getNbPieces(self):
        piece = self.ids["spinnerPieces"].text
        self.joueurQuiAJoue = ""

        if nb_coups%2 == 0 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur1

        elif nb_coups%2 == 0 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups%2 == 1 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups%2 == 1 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur1

        if piece == "Carré":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["carre"])
        elif piece == "Rond":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["rond"])
        elif piece == "Triangle":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["triangle"])
        else:
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["croix"])

    def mettrePieceDansPlateau(self, piece, id):
        for ligne in acces_plateau.plateau:
            if id in ligne:
                position = ligne.index(id)
                ligne[position] = piece

class MenuHistorique(Screen):

    def creerSelect(self):
        self.ids["joueurSelectionne"].values = acces_joueur1.pseudo, acces_joueur2.pseudo

    def getWinrate(self, array_param):
        self.joueur = self.ids["joueurSelectionne"].text
        nb_parties = len(array_param)
        nb_victoires = 0
        for partie in array_param:
            if (partie[0] == self.joueur and partie[2] == 1) or (
                    partie[1] == self.joueur and partie[2] == 2):
                nb_victoires += 1
        return round((nb_victoires / nb_parties) * 100, 2)

    def convertirDate(self, str_date):
        date = str_date.split("-")
        return str(date[2] + "-" + date[1] + "-" + date[0])

    def getHistorique(self):
        self.removeHistorique()
        self.joueur = self.ids["joueurSelectionne"].text
        conn = sqlite3.connect("QuantikGame/historique.db")
        cli = conn.cursor()
        cli.execute("SELECT Joueur1, Joueur2, Gagnant, NbCoup, DatePartie FROM Historique WHERE Joueur1 = '" + self.joueur + "' OR Joueur2 ='" + self.joueur + "'")
        parties_list = cli.fetchall()
        layout = self.ids["historique"]
        for partie in parties_list:
            if partie[0] == self.joueur and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[0] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == self.joueur and partie[2] == 1:
                label = Label(text='[color=1EB806]Victoire contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 1:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[0] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == self.joueur and partie[2] == 2:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 2:
                label = Label(text='[color=1EB806]Victoire contre ' + partie[0] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
        if len(parties_list) != 0:
            layout = self.ids["winrate"]
            label = Label(text='[color=d6ab32]Winrate : ' + str(self.getWinrate(parties_list)) + ' %[/color]',
                          markup=True, font_size=30, size_hint=(0.3, 0.08))
            layout.add_widget(label)

    def removeHistorique(self):
        layout = self.ids["historique"]
        layout.clear_widgets()
        layout = self.ids["winrate"]
        layout.clear_widgets()

    def fermerHistorique(self):
        self.removeHistorique()
        self.joueur = self.ids["joueurSelectionne"].text = "Joueurs"

    def ajouterDonnees(self, joueur1, joueur2, gagnant, coup):
        conn = sqlite3.connect("QuantikGame/historique.db")
        cli = conn.cursor()
        dateYear = date.today().strftime('%Y')
        dateMonth = date.today().strftime('%m')
        dateDay = date.today().strftime('%d')

        dateGame = str(dateYear + "-" + dateMonth + "-" + dateDay)
        cli.execute("INSERT INTO Historique(Joueur1, Joueur2, Gagnant, NbCoup, DatePartie) VALUES ('" + joueur1 + "','" + joueur2 + "'," + gagnant + "," + coup + ",'" + dateGame + "')")
        conn.commit()

screen_manager = ScreenManager(transition=NoTransition())

screen_manager.add_widget(MenuPrincipale())
screen_manager.add_widget(MenuRegles())
screen_manager.add_widget(MenuJouer())
screen_manager.add_widget(MenuHistorique())


class QuantikGame(App):
    def build(self):
        return screen_manager


class PartieGraphique():

    def __init__(self, joueur1, joueur2):
        self.__joueur1 = joueur1
        self.__joueur2 = joueur2
        self.__plateau = Plateau()

    def start(self):
        global nb_coups
        nb_coups = 0
        global acces_joueur1
        acces_joueur1 = Joueur(self.__joueur1)
        global acces_joueur2
        acces_joueur2 = Joueur(self.__joueur2)
        global acces_plateau
        acces_plateau = self.__plateau