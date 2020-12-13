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

Window.hide()

Builder.load_file("QuantikGame/interface.kv")


class MenuPrincipale(Screen):
    pass

class MenuRegles(Screen):
    pass


class MenuJouer(Screen):

    def commencerPartie(self):
        nb_random = int(random.uniform(0, 2))
        if nb_random == 0:
            self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo
            acces_joueur1.couleur = "rouge"
            acces_joueur2.couleur = "bleu"
        else:
            self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            acces_joueur2.couleur = "rouge"
            acces_joueur1.couleur = "bleu"

    def deroulementPartie(self, nb_random):
        if nb_random == 0:
            while True:
                self.jouerTour(acces_joueur1.pseudo, acces_joueur1.pieces)
                if self.__plateau.testVictoire(acces_joueur1.pseudo):
                    break;
                self.jouerTour(acces_joueur2.pseudo, acces_joueur2.pieces)
                if self.__plateau.testVictoire(acces_joueur2.pseudo):
                    break;
        else:
            while True:
                self.jouerTour(acces_joueur2.pseudo, acces_joueur2.pieces)
                if self.__plateau.testVictoire(acces_joueur2.pseudo):
                    break;
                self.jouerTour(acces_joueur1.pseudo, acces_joueur1.pieces)
                if self.__plateau.testVictoire(acces_joueur1.pseudo):
                    break;

    def jouerTour(self, joueur, piecesJoueur):
        self.joue = True
        self.ids["tour"].text = "C'est au tour de\n" + joueur


    def mettrePiece(self):
        pass

    def getNbPieces(self):
        piece = self.ids["spinnerPieces"].text
        if piece == "Carré":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueur.pieces["carre"])
        elif piece == "Rond":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueur.pieces["rond"])
        elif piece == "Triangle":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueur.pieces["triangle"])
        else:
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueur.pieces["croix"])

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
        cli.execute(
            "SELECT Joueur1, Joueur2, Gagnant, NbCoup, DatePartie FROM Historique WHERE Joueur1 = '" + self.joueur + "' OR Joueur2 ='" + self.joueur + "'")
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
        global acces_joueur1
        acces_joueur1 = Joueur(self.__joueur1)
        global acces_joueur2
        acces_joueur2 = Joueur(self.__joueur2)
        global acces_plateau
        acces_plateau = self.__plateau
