import random
from plateau.plateau import Plateau
from joueur.joueur import Joueur
from QuantikGame.partieGraphique import PartieGraphique
from QuantikGame.partieGraphique import QuantikGame
from kivy.core.window import Window
from QuantikGame.partieGraphique import MenuHistorique



class PartieConsole:

    # Définition du premier joueur + Utilisation des class Joueur et Plateau
    def __init__(self):
        self.__random = int(random.uniform(0, 2))
        self.__Joueur1 = ""
        self.__Joueur2 = ""
        self.__plateau = Plateau()

    # Déroulement d'un tour, elle prend en paramètre le nom du joueur ainsi que les pièces dont il dispose.
    def jouer_tour(self, joueur, pieces_joueur):
        print("Au tour de " + joueur)
        print('Vous avez {} "carre", {} "rond", {} "triangle", {} "croix" '.format(pieces_joueur["carre"],
                                                                                   pieces_joueur["rond"],
                                                                                   pieces_joueur["triangle"],
                                                                                   pieces_joueur["croix"]))
        print("Insérer comme ceci : nom_de_la_piece, ID_de_la_case")

        placement_string = input()
        placement_list = placement_string.split(", ")
        if len(placement_list) != 2:
            while True:
                placement_str = input()
                placement_list = placement_str.split(", ")
                if len(placement_list) == 2 and len(placement_list[1]) == 2:
                    break
                else:
                    print("Veuiller respecter cette syntaxe : nom_de_la_piece, ID_de_la_case")

        if len(placement_list[1]) == 2:
            while True:
                if placement_list[0] in pieces_joueur and pieces_joueur[placement_list[0]] > 0 and (
                        placement_list[1] in self.__plateau.plateau[0] or placement_list[1] in
                        self.__plateau.plateau[1] or placement_list[1] in
                        self.__plateau.plateau[2] or placement_list[1] in self.__plateau.plateau[3]):
                    pieces_joueur[placement_list[0]] = pieces_joueur[placement_list[0]] - 1
                    break
                else:
                    print(
                        "Vous avez tapé un mauvais nom de piece, un emplacement déjà pris, un mauvais id de case ou "
                        "vous n'avez plus de {}, veuillez les réinsérer :".format(
                            placement_list[0]))
                    placement_str = input()
                    placement_list = placement_str.split(", ")

            for ligne in self.__plateau.plateau:
                if placement_list[1] in ligne:
                    position = ligne.index(placement_list[1])
                    ligne[position] = placement_list[0]
            print("\n" * 25)
            print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(self.__plateau.plateau[0], self.__plateau.plateau[1],
                                                                 self.__plateau.plateau[2], self.__plateau.plateau[3]))

    # Déroulement d'un partie complete, elle lance les tours de jeu un par un pour que les joueurs jouent chacun à
    # leur tour

    def deroulement_partie(self):
        global nb_coups
        print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(self.__plateau.plateau[0], self.__plateau.plateau[1],
                                                             self.__plateau.plateau[2], self.__plateau.plateau[3]))
        if self.__random == 0:
            while True:
                self.jouer_tour(self.__Joueur1.pseudo, self.__Joueur1.pieces)
                nb_coups += 1
                if self.__plateau.testVictoire(self.__Joueur1.pseudo) or self.__plateau.testEgualite():
                    MenuHistorique().ajouter_donnees(self.__Joueur1.pseudo, self.__Joueur2.pseudo, str(1), str(nb_coups))
                    break
                self.jouer_tour(self.__Joueur2.pseudo, self.__Joueur2.pieces)
                nb_coups += 1
                if self.__plateau.testVictoire(self.__Joueur2.pseudo) or self.__plateau.testEgualite():
                    MenuHistorique().ajouter_donnees(self.__Joueur1.pseudo, self.__Joueur2.pseudo, str(2), str(nb_coups))
                    break
        else:
            while True:
                self.jouer_tour(self.__Joueur2.pseudo, self.__Joueur2.pieces)
                nb_coups += 1
                if self.__plateau.testVictoire(self.__Joueur2.pseudo) or self.__plateau.testEgualite():
                    MenuHistorique().ajouter_donnees(self.__Joueur1.pseudo, self.__Joueur2.pseudo, str(2), str(nb_coups))
                    break
                self.jouer_tour(self.__Joueur1.pseudo, self.__Joueur1.pieces)
                nb_coups += 1
                if self.__plateau.testVictoire(self.__Joueur1.pseudo) or self.__plateau.testEgualite():
                    MenuHistorique().ajouter_donnees(self.__Joueur1.pseudo, self.__Joueur2.pseudo, str(1), str(nb_coups))
                    break

    def demarer_programme_console(self):
        joueur1 = input("Veuillez entrer le pseudo du premier joueur :")
        joueur2 = input("Veuillez entrer le pseudo du deuxième joueur :")
        self.__Joueur1 = Joueur(joueur1)
        self.__Joueur2 = Joueur(joueur2)
        print("\n" * 25)
        self.deroulement_partie()

    def lancement_application(self):
        print("\n" * 25)
        while True:
            interface = input("Voulez jouer en console ou avec l'interface graphique ('console' ou 'graphique'):")
            if interface == "console":
                global nb_coups
                nb_coups=0
                print("\n" * 25)
                self.demarer_programme_console()
                break
            elif interface == "graphique":
                print("\n" * 25)
                while True:
                    joueur1 = input("Veuillez entrer le pseudo du joueur 1 (maximum 15 caractères):")
                    if len(joueur1) <= 15:
                        break
                while True:
                    joueur2 = input("Veuillez entrer le pseudo du joueur 2 (maximum 15 caractères):")
                    if len(joueur2) <= 15:
                        break
                PartieGraphique(joueur1, joueur2).start()
                Window.show()
                QuantikGame().run()
                break
