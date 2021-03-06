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

            PRE : le paramètre est un booléan qui permet oui ou non de verrouiller le plateau.

            POST : Lors d'une victoire, le plateau est verrouiller afin que les joueurs ne puissent plus poser de pièces
                   dessus.

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
        """
            Fonction qui permet de réinitialiser le plateau, le déverrouille, enlever le message de victoire,
            réinitialiser les pièces des joueurs et de remettre le nom des pièces dans le sélectionneur.

            PRE : -

            POST : Remet le plateau à sa valeur initial ainsi que les dictionnaires contenant les pièces des joueurs.

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
        """
            Fonction qui permet de réinitialiser le nombre de coup, décider qui commence et attrivuer les couleurs aux
            joueurs.

            PRE : -
            POST : Attribue une couleur aléatoire à un joueur et initialise le nombre de coup à 0.

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
        """
            Fonction qui permet de pièce sur le plateau de l'interface kivy et vérifier si cela produit une victoire

            PRE : Le paramètre de la fonction est l'id de case ou le joueur désire mettre sa pièce.

            POST : Place la pièce sur la case demandée en paramère si celle n'est pas déjà occupée et si le joueur
                   dispose encore de ce type de pièce.
                   Après chaque pièce posée, un test de victoire est effectué.

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

            POST : Verifie que le joueur possède bien la pièce qu'il désire posé, si c'est le cas décrémente

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
        """
            Fonction qui permet de mettre une pièce dans la variable acces_plateau.plateau

            PRE : Cette fonction possède deux paramètres, le premier s'appel "piece" il correspond au nom de la pièce
                  que le joueur souhaite placé et le second s'appel id et correspond à la case du plateau ou le joueur
                  désire placé sa pièce.

            POST : Met la pièce sur la bonne case dans le plateau.

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
        """
            Fonction qui permet d'ajouter un sélect sur la page Historique de l'application.

        """
        self.ids["joueur_selectionne"].values = acces_joueur1.pseudo, acces_joueur2.pseudo

    def get_winrate(self, array_param, pseudo):
        """
            Fonction qui permet de calculer le winrate d'un joueur en fonction des parties de son historiques.

            PRE :  Le paramètre "array_param" est une liste qui contient tout les parties et le paramètre "pseudo" est
                   le pseudo du joueur dont on désire le winrate.

            POST : Renvoie le winrate en pourcentage sur base du nombre de partie gagnée par rapport au nombre de partie
                   jouée.

            RAISES : TypeError si type(array_param) != list

        """
        if type(array_param) != list:
            raise TypeError

        nb_parties = len(array_param)
        nb_victoires = 0
        for partie in array_param:
            if (partie[0] == pseudo and partie[2] == 1) or (
                    partie[1] == pseudo and partie[2] == 2):
                nb_victoires += 1
        return round((nb_victoires / nb_parties) * 100, 2)

    def convertir_date(self, str_date):
        """Fonction qui permet de changer le format d'une date.

            PRE : Le paramètre de la fonction est une chaine de caractère conetenant la date sous ce format : "2020-12-02"

            POST : Renvoie la date après modification, cela donne "02-12-2020"

            RAISES : TypeError si type(str_date) != list

        """
        if type(str_date) != str:
            raise TypeError
        date = str_date.split("-")
        return str(date[2] + "-" + date[1] + "-" + date[0])

    def get_historique(self):
        """Fonction qui permet d'écrire l'historique dans l'interface graphique à partir de la base de données.

            PRE : -

            POST : Récupération de l'historique du joueur sélectionner dans le select et affichage dynamique.

            RAISES : -

        """
        self.remove_historique()
        self.joueur = self.ids["joueur_selectionne"].text
        try:
            conn = sqlite3.connect("QuantikGame/historique.db")
        except sqlite3.Error as er:
            print('Erreure : ' + (' '.join(er.args)))

        cli = conn.cursor()
        try:
            cli.execute(
                "SELECT Joueur1, Joueur2, Gagnant, NbCoup, DatePartie FROM Historique WHERE Joueur1 = '" + self.joueur + "' OR Joueur2 ='" + self.joueur + "'")
        except sqlite3.Error as er:
            print('Erreure : ' + (' '.join(er.args)))

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
            label = Label(text='[color=d6ab32]Winrate : ' + str(self.get_winrate(parties_list, self.joueur)) + ' %[/color]',
                          markup=True, font_size=30, size_hint=(0.3, 0.08))
            layout.add_widget(label)

    def remove_historique(self):
        """Fonction qui permet d'enlever toutes les données qui se trouvent dans la page "historique" de l'interface
        graphique.

            PRE : -

            POST : Clear tout ce qui se trouve dans la page historique dans les champs boxs portant les ids "historique"
                   et "winrate".

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
            POST : Appel la fontion self.remove_historique() et met dans le select la valeur "Joueurs"
            RAISES : -

        """
        self.remove_historique()
        self.ids["joueur_selectionne"].text = "Joueurs"

    def ajouter_donnees(self, joueur1, joueur2, gagnant, coup):
        """Fonction qui permet d'ajouter des données dans la base de données.

            PRE : Cette fonction possède quatre paramètre, "joueur1" qui est le pseudo du premier joueur, "joueur2" qui
                  est le pseudo du second joueur, "gagnant" qui est le numéro du vainqueur et "coup" qui est le nombre
                  de coup de la partie.

            POST : Insert les données dans la base de donnée.

            RAISES : TypeError si type(str_date) != list

        """
        try:
            conn = sqlite3.connect("QuantikGame/historique.db")
        except sqlite3.Error as er:
            print('Erreure : ' + (' '.join(er.args)))

        cli = conn.cursor()
        dateYear = date.today().strftime('%Y')
        dateMonth = date.today().strftime('%m')
        dateDay = date.today().strftime('%d')

        dateGame = str(dateYear + "-" + dateMonth + "-" + dateDay)
        try:
            cli.execute(
                "INSERT INTO Historique(Joueur1, Joueur2, Gagnant, NbCoup, DatePartie) VALUES ('" + joueur1 + "','" + joueur2 + "'," + gagnant + "," + coup + ",'" + dateGame + "')")
        except sqlite3.Error as er:
            print('Erreure : ' + (' '.join(er.args)))

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

    @property
    def joueur1(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__joueur1 qui est une chaine de caractère contenant le pseudo
                   du joueur1

        """
        return self.__joueur1

    @property
    def joueur2(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__joueur2 qui est une chaine de caractère contenant le pseudo
                   du joueur2

        """
        return self.__joueur2

    @property
    def plateau(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__plateau qui est une liste de listes.

        """
        return self.__plateau

    def start(self):
        """
            Cette fonction permet de démarer la partie graphique.

            PRE : -

            POST : Met le nombre de coup à sa valeur initial 0, et mets en variable global les instances de la class
                   Joueur ainsi que de la class Plateau.

        """
        global nb_coups
        nb_coups = 0
        global acces_joueur1
        acces_joueur1 = Joueur(self.__joueur1)
        global acces_joueur2
        acces_joueur2 = Joueur(self.__joueur2)
        global acces_plateau
        acces_plateau = self.__plateau
