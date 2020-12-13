#  Il s'agit de la class Partie qui permet de créer tout le déroulement de la partie.
#
# Maxime Lits, Matthew Everard

import random
from plateau.plateau import Plateau
from joueur.joueur import Joueur
from QuantikGame.fenetre import PartieGraphique
from QuantikGame.fenetre import QuantikGame
from kivy.core.window import Window
import threading

class PartieConsole():

# Définition du premier joueur + Utilisation des class Joueur et Plateau
    def __init__(self):
        self.__random = int(random.uniform(0, 2))
        self.__Joueur1 = ""
        self.__Joueur2 = ""
        self.__plateau = Plateau()

# Déroulement d'un tour, elle prend en paramètre le nom du joueur ainsi que les pièces dont il dispose.
    def jouerTour(self, joueur, piecesJoueur):
        print("Au tour de " + joueur)
        print('Vous avez {} "carre", {} "rond", {} "triangle", {} "croix" '.format(piecesJoueur["carre"], piecesJoueur["rond"],  piecesJoueur["triangle"], piecesJoueur["croix"]))
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
                if placement_list[0] in piecesJoueur and piecesJoueur[placement_list[0]] > 0 and (
                        placement_list[1] in self.__plateau.plateau[0] or placement_list[1] in self.__plateau.plateau[1] or placement_list[1] in
                        self.__plateau.plateau[2] or placement_list[1] in self.__plateau.plateau[3]):
                    piecesJoueur[placement_list[0]] = piecesJoueur[placement_list[0]] - 1
                    break
                else:
                    print("Vous avez tapé un mauvais nom de piece, un emplacement déjà pris, un mauvais id de case ou vous n'avez plus de {}, veuillez les réinsérer :".format(    placement_list[0]))
                    placement_str = input()
                    placement_list = placement_str.split(", ")

            for ligne in self.__plateau.plateau:
                if placement_list[1] in ligne:
                    position = ligne.index(placement_list[1])
                    ligne[position] = placement_list[0]
            print("\n" * 25)
            print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(self.__plateau.plateau[0], self.__plateau.plateau[1], self.__plateau.plateau[2], self.__plateau.plateau[3]))

# Déroulement d'un partie complete, elle lance les tours de jeu un par un pour que les joueurs jouent chacun à leur tour
    def deroulementPartie(self):
        print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(self.__plateau.plateau[0], self.__plateau.plateau[1], self.__plateau.plateau[2], self.__plateau.plateau[3]))
        if self.__random == 0:
            while True:
                self.jouerTour(self.__Joueur1.pseudo, self.__Joueur1.pieces)
                if self.__plateau.testVictoire(self.__Joueur1.pseudo) or self.__plateau.testEgualite():
                    break;
                self.jouerTour(self.__Joueur2.pseudo, self.__Joueur2.pieces)
                if self.__plateau.testVictoire(self.__Joueur2.pseudo) or self.__plateau.testEgualite():
                    break;
        else:
            while True:
                self.jouerTour(self.__Joueur2.pseudo, self.__Joueur2.pieces)
                if self.__plateau.testVictoire(self.__Joueur2.pseudo) or self.__plateau.testEgualite():
                    break;
                self.jouerTour(self.__Joueur1.pseudo, self.__Joueur1.pieces)
                if self.__plateau.testVictoire(self.__Joueur1.pseudo) or self.__plateau.testEgualite():
                    break;


    def demarerProgrammeConsole(self):
        joueur1 = input("Veuillez entrer le pseudo du premier joueur :")
        joueur2 = input("Veuillez entrer le pseudo du deuxième joueur :")
        self.__Joueur1 = Joueur(joueur1)
        self.__Joueur2 = Joueur(joueur2)
        print("\n" * 25)
        self.deroulementPartie()

    def lancementApplication(self):
        print("\n" * 25)
        while True:
            interface = input("Voulez jouer en console ou avec l'interface graphique ('console' ou 'graphique'):")
            if interface == "console":
                print("\n" * 25)
                self.demarerProgrammeConsole()
                break
            elif interface == "graphique":
                print("\n" * 25)
                while True:
                    joueur1 = input("Veuillez entrer le pseudo du joueur 1 (maximum 15 caractères):")
                    if len(joueur1) <= 15:
                        break;
                while True:
                    joueur2 = input("Veuillez entrer le pseudo du joueur 2 (maximum 15 caractères):")
                    if len(joueur2) <= 15:
                        break;
                PartieGraphique(joueur1, joueur2).start()
                Window.show()
                QuantikGame().run()
                break