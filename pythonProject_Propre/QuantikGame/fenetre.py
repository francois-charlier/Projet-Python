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
import sqlite3
import threading
from joueur.joueur import Joueur
import socket
import select

Window.hide()

Builder.load_file("QuantikGame/interface.kv")


class MenuPrincipale(Screen):
    pass


class Connection():
    def __init__(self):
        self.__server = ("", 12800)
        self.__client = ("localhost", 12800)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startServer(self):
        self.__sock.bind(self.__server)
        while True:
            self.__sock.listen()
            conn, addr = self.__sock.accept()
            print("client connecté")
        conn.close()
        self.__sock.close()

    def startClient(self):
        self.__sock.connect(self.__client)

    def demarerSocket(self):

        try:
            th2 = threading.Thread(target=self.startClient())
            th2.start()

        except ConnectionRefusedError:
            th3 = threading.Thread(target=self.startServer())
            th3.start()

class MenuRegles(Screen):
    pass


class MenuJouer(Screen):

    def envoyerData(self):
        pass

    def demarrerConnection(self):
        Connection().demarerSocket()

    def getNbPieces(self):
        piece = self.ids["spinnerPieces"].text
        if piece == "Carré":
            self.ids["nbPieces"].text = "Nombre : " + str(acces_joueur.pieces["carre"])
        elif piece == "Rond":
            self.ids["nbPieces"].text = "Nombre : " + str(acces_joueur.pieces["rond"])
        elif piece == "Triangle":
            self.ids["nbPieces"].text = "Nombre : " + str(acces_joueur.pieces["triangle"])
        else:
            self.ids["nbPieces"].text = "Nombre : " + str(acces_joueur.pieces["croix"])


class MenuHistorique(Screen):
    def getWinrate(self, array_param):
        nb_parties = len(array_param)
        nb_victoires = 0
        for partie in array_param:
            if (partie[0] == acces_joueur.pseudo and partie[2] == 1) or (
                    partie[1] == acces_joueur.pseudo and partie[2] == 2):
                nb_victoires += 1
        return round((nb_victoires / nb_parties) * 100, 2)

    def convertirDate(self, str_date):
        date = str_date.split("-")
        return str(date[2] + "-" + date[1] + "-" + date[0])

    def getHistorique(self):
        conn = sqlite3.connect("QuantikGame/historique.db")
        cli = conn.cursor()
        cli.execute(
            "SELECT Joueur1, Joueur2, Gagnant, NbCoup, DatePartie FROM Historique WHERE Joueur1 = '" + acces_joueur.pseudo + "' OR Joueur2 ='" + acces_joueur.pseudo + "'")
        parties_list = cli.fetchall()
        layout = self.ids["historique"]
        for partie in parties_list:
            if partie[0] == acces_joueur.pseudo and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == acces_joueur.pseudo and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[0] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == acces_joueur.pseudo and partie[2] == 1:
                label = Label(text='[color=1EB806]Victoire contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == acces_joueur.pseudo and partie[2] == 1:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[0] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == acces_joueur.pseudo and partie[2] == 2:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[1] + ' le ' + self.convertirDate(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == acces_joueur.pseudo and partie[2] == 2:
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


screen_manager = ScreenManager(transition=NoTransition())

screen_manager.add_widget(MenuPrincipale())
screen_manager.add_widget(MenuRegles())
screen_manager.add_widget(MenuJouer())
screen_manager.add_widget(MenuHistorique())


class QuantikGame(App):
    def build(self):
        return screen_manager


class PartieGraphique():

    def __init__(self, joueur):
        self.__joueur = joueur

    def start(self):
        global acces_joueur
        acces_joueur = Joueur(self.__joueur)
