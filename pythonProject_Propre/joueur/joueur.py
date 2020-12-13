#
# Il s'agit de la class Joueur qui permet de stocker les pièces du joueur
#
# Maxime Lits

from plateau.plateau import Plateau

class Joueur():

    def __init__(self, pseudo):

        self.__couleur = ""

        self.__pieces = {"carre":2,
                          "rond":0,
                      "triangle":2,
                         "croix":1}

        self.__pseudo = pseudo

        self.__plateau = Plateau()


    @property
    def pieces(self):
        return self.__pieces

    @property
    def pseudo(self):
        return self.__pseudo

    @property
    def couleur(self):
        return self.__couleur

    @property
    def plateau(self):
        return self.__plateau