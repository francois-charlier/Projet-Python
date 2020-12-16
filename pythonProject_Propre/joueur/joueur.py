class Joueur:

    def __init__(self, pseudo):
        self.__couleur = ""

        self.__pieces = {"carre": 2,
                         "rond": 2,
                         "triangle": 2,
                         "croix": 2}

        self.__pseudo = pseudo

    @property
    def pieces(self):
        return self.__pieces

    @pieces.setter
    def pieces(self, value):
        self.__pieces = value

    @property
    def pseudo(self):
        return self.__pseudo

    @property
    def couleur(self):
        return self.__couleur

    @couleur.setter
    def couleur(self, value):
        self.__couleur = value
