from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
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

    def verrouiller_plateau(self, param):
        """Fonction qui permet verrouiller le plateau de la partie graphique en mettant toutes les cases en disabled

            PRE : param === bool
            POST : -
            RAISES : TypeError si type(param) != bool

        """
        if type(param) != bool:
            raise TypeError

        for ligne in acces_plateau.plateau:
            for case in ligne:
                if len(case) == 2:
                    self.ids[case].disabled = param
                    self.ids[case].background_disabled_normal = "QuantikGame/imgs/jouer/cell.png"
                    self.ids[case].background_disabled_down = "QuantikGame/imgs/jouer/cell.png"

    def retour_menu(self):
        """Fonction qui permet de réinitialiser le plateau, le déverrouille, enlever le message de victoire,
        réinitialiser les pièces des joueurs et de remettre le nom des pièces dans le sélectionneur.

            PRE : -
            POST : -
            RAISES : -

        """
        acces_plateau.plateau = [["A1", "A2", "A3", "A4"],
                                 ["B1", "B2", "B3", "B4"],
                                 ["C1", "C2", "C3", "C4"],
                                 ["D1", "D2", "D3", "D4"]]

        self.verrouiller_plateau(False)
        self.ids["victoire"].text = ""
        self.ids["spinnerPieces"].values = ("Carré", "Rond", "Triangle", "Croix")
        acces_joueur1.pieces = {"carre": 2,
                                "rond": 2,
                                "triangle": 2,
                                "croix": 2}

        acces_joueur2.pieces = {"carre": 2,
                                "rond": 2,
                                "triangle": 2,
                                "croix": 2}

    def commencer_partie(self):
        """Fonction qui permet de réinitialiser le nombre de coup, décider qui commence et attrivuer les couleurs aux
        joueurs.

            PRE : -
            POST : -
            RAISES : -

        """
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

    def mettre_piece(self, id):
        """Fonction qui permet de pièce sur le plateau de l'interface kivy et vérifier si cela produit une victoire

            PRE : id === str et len(id) == 2
            POST : -
            RAISES : TypeError si type(id) != str ou len(id) != 2

        """
        if type(id) != str or len(id) != 2:
            raise TypeError

        global nb_coups
        self.joueurQuiAJoue = ""

        if nb_coups % 2 == 0 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur1

        elif nb_coups % 2 == 0 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups % 2 == 1 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups % 2 == 1 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur1

        self.couleur = self.joueurQuiAJoue.couleur

        if (self.ids["spinnerPieces"].text == "Carré") and (self.joueurQuiAJoue.pieces["carre"] > 0):
            self.ids[id].disabled = True
            self.ids[id].background_disabled_normal = "QuantikGame/imgs/jouer/carre_" + self.couleur + ".png"
            self.ids[id].background_disabled_down = "QuantikGame/imgs/jouer/carre_" + self.couleur + ".png"
            self.joueurQuiAJoue.pieces["carre"] -= 1
            nb_coups += 1
            self.ids["spinnerPieces"].text = "Pièces"
            self.ids["nbPieces"].text = ""
            if self.joueurQuiAJoue.pseudo == acces_joueur2.pseudo:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur2.pseudo
            else:
                self.ids["tour"].text = "C'est au tour de\n" + acces_joueur1.pseudo

            self.mettre_piece_dans_plateau("carre", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

        elif (self.ids["spinnerPieces"].text == "Rond") and (self.joueurQuiAJoue.pieces["rond"] > 0):
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
            self.mettre_piece_dans_plateau("rond", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

        elif (self.ids["spinnerPieces"].text == "Triangle") and (self.joueurQuiAJoue.pieces["triangle"] > 0):
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
            self.mettre_piece_dans_plateau("triangle", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

        elif (self.ids["spinnerPieces"].text == "Croix") and (self.joueurQuiAJoue.pieces["croix"] > 0):
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
            self.mettre_piece_dans_plateau("croix", id)
            if acces_joueur1.pseudo == self.joueurQuiAJoue.pseudo:
                if acces_plateau.testVictoire(acces_joueur2.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur2.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(2), str(nb_coups))
            else:
                if acces_plateau.testVictoire(acces_joueur1.pseudo):
                    self.ids["victoire"].text = "Victoire de\n " + acces_joueur1.pseudo + " !!!"
                    self.ids["victoire"].color = (0.1686, 0.5764, 0.2823, 1)
                    self.verrouiller_plateau(True)
                    self.ids["spinnerPieces"].text = "Pièces"
                    self.ids["spinnerPieces"].values = ""
                    MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(1), str(nb_coups))
            if nb_coups == 16:
                self.ids["victoire"].text = "Egalité !!!"
                self.ids["victoire"].color = (0.0117, 0.0156, 0.3725, 1)
                self.ids["spinnerPieces"].text = "Pièces"
                self.ids["spinnerPieces"].values = ""
                MenuHistorique().ajouter_donnees(acces_joueur1.pseudo, acces_joueur2.pseudo, str(0), str(nb_coups))

    def get_nb_pieces(self):
        """Fonction qui permet de savoir qui joue et de lui enlever la pièce jouée.

            PRE : -
            POST : -
            RAISES : -

        """
        piece = self.ids["spinnerPieces"].text
        self.joueurQuiAJoue = ""

        if nb_coups % 2 == 0 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur1

        elif nb_coups % 2 == 0 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups % 2 == 1 and acces_joueur1.couleur == "rouge":
            self.joueurQuiAJoue = acces_joueur2

        elif nb_coups % 2 == 1 and acces_joueur1.couleur == "bleu":
            self.joueurQuiAJoue = acces_joueur1

        if piece == "Carré":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["carre"])
        elif piece == "Rond":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["rond"])
        elif piece == "Triangle":
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["triangle"])
        else:
            self.ids["nbPieces"].text = "Nombre : " + str(self.joueurQuiAJoue.pieces["croix"])

    def mettre_piece_dans_plateau(self, piece, id):
        """Fonction qui permet de mettre une pièce dans la variable acces_plateau.plateau

            PRE : piece === str, id === str et len(id) == 2
            POST : -
            RAISES : TypeError si type(piece) != str ou type(id) != str ou len(id) != 2

        """
        if type(piece) != str or type(id) != str or len(id) != 2:
            raise TypeError

        for ligne in acces_plateau.plateau:
            if id in ligne:
                position = ligne.index(id)
                ligne[position] = piece


class MenuHistorique(Screen):

    def creer_select(self):

        self.ids["joueur_selectionne"].values = acces_joueur1.pseudo, acces_joueur2.pseudo

    def get_winrate(self, array_param):
        """Fonction qui permet de calculer le winrate d'un joueur en fonction des parties de son historiques.

            PRE : array_param === list
            POST : Renvoie le winrate en pourcentage
            RAISES : TypeError si type(array_param) != list

        """
        if type(array_param) != list:
            raise TypeError

        self.joueur = self.ids["joueur_selectionne"].text
        nb_parties = len(array_param)
        nb_victoires = 0
        for partie in array_param:
            if (partie[0] == self.joueur and partie[2] == 1) or (
                    partie[1] == self.joueur and partie[2] == 2):
                nb_victoires += 1
        return round((nb_victoires / nb_parties) * 100, 2)

    def convertir_date(self, str_date):
        """Fonction qui permet de changer le format d'une date.

            PRE : str_date === str
            POST : Renvoie la date après modification
            RAISES : TypeError si type(str_date) != list

        """
        if type(str_date) != list:
            raise TypeError
        date = str_date.split("-")
        return str(date[2] + "-" + date[1] + "-" + date[0])

    def get_historique(self):
        """Fonction qui permet d'écrire l'historique dans l'interface graphique à partir de la base de données.

            PRE : -
            POST : -
            RAISES : -

        """
        self.remove_historique()
        self.joueur = self.ids["joueur_selectionne"].text
        conn = sqlite3.connect("QuantikGame/historique.db")
        cli = conn.cursor()
        cli.execute(
            "SELECT Joueur1, Joueur2, Gagnant, NbCoup, DatePartie FROM Historique WHERE Joueur1 = '" + self.joueur + "' OR Joueur2 ='" + self.joueur + "'")
        parties_list = cli.fetchall()
        layout = self.ids["historique"]
        for partie in parties_list:
            if partie[0] == self.joueur and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[1] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 0:
                label = Label(text='[color=0000ff]Egalité contre ' + partie[0] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == self.joueur and partie[2] == 1:
                label = Label(text='[color=1EB806]Victoire contre ' + partie[1] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 1:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[0] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[0] == self.joueur and partie[2] == 2:
                label = Label(text='[color=ff0000]Défaite contre ' + partie[1] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
            elif partie[1] == self.joueur and partie[2] == 2:
                label = Label(text='[color=1EB806]Victoire contre ' + partie[0] + ' le ' + self.convertir_date(
                    partie[4]) + ' en ' + str(partie[3]) + ' coups[/color]', markup=True, font_size=30)
                layout.add_widget(label)
        if len(parties_list) != 0:
            layout = self.ids["winrate"]
            label = Label(text='[color=d6ab32]Winrate : ' + str(self.get_winrate(parties_list)) + ' %[/color]',
                          markup=True, font_size=30, size_hint=(0.3, 0.08))
            layout.add_widget(label)

    def remove_historique(self):
        """Fonction qui permet d'enlever toutes les données qui se trouvent dans la page "historique" de l'interface
        graphique.

            PRE : -
            POST : -
            RAISES : -

        """
        layout = self.ids["historique"]
        layout.clear_widgets()
        layout = self.ids["winrate"]
        layout.clear_widgets()

    def fermer_historique(self):
        """Fonction qui permet d'appeller la fonction remove_historique et de changer le text du sélectionneur de la
        page historique.

            PRE : -
            POST : -
            RAISES : -

        """
        self.remove_historique()
        self.joueur = self.ids["joueur_selectionne"].text = "Joueurs"

    def ajouter_donnees(self, joueur1, joueur2, gagnant, coup):
        """Fonction qui permet d'ajouter des données dans la base de données.

            PRE : joueur1 === str, joueur2 === str, gagnant === int, coup === int
            POST : -
            RAISES : TypeError si type(str_date) != list

        """
        if type(joueur1) != str or type(joueur2) != str or type(gagnant) != int or type(coup) != int:
            raise TypeError
        conn = sqlite3.connect("QuantikGame/historique.db")
        cli = conn.cursor()
        dateYear = date.today().strftime('%Y')
        dateMonth = date.today().strftime('%m')
        dateDay = date.today().strftime('%d')

        dateGame = str(dateYear + "-" + dateMonth + "-" + dateDay)
        cli.execute(
            "INSERT INTO Historique(Joueur1, Joueur2, Gagnant, NbCoup, DatePartie) VALUES ('" + joueur1 + "','" + joueur2 + "'," + gagnant + "," + coup + ",'" + dateGame + "')")
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
