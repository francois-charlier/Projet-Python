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
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__pieces qui est un disctionnaire contenant les pièces du joueur.

        """
        return self.__pieces

    @pieces.setter
    def pieces(self, value):
        """
            PRE : Le paramètre de cette fonction est un dictionnaire contenant les pièces du joueur pour une nouvelle
                  partie.

            POST : Attribue la valeur du paramètre à l'attribut self.__pieces.

        """
        self.__pieces = value

    @property
    def pseudo(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__pseudo qui est une chaine de caractère conetenant le pseudo
                   du joueur.

        """
        return self.__pseudo

    @property
    def couleur(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__couleur qui est une chaine de caractère conetenant la couleur
                   des pièces du joueur.

        """
        return self.__couleur

    @couleur.setter
    def couleur(self, value):
        """
            PRE : Le paramètre de cette fonction est une chaine de caractère qui est la couleur du joueur.

            POST : Attribue la valeur du paramètre à l'attribut self.__couleur.

        """
        self.__couleur = value
