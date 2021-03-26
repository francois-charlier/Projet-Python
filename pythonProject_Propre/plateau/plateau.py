class Plateau:

    # Definition du plateau du jeu
    def __init__(self):
        self.__plateau = [["A1", "A2", "A3", "A4"],
                          ["B1", "B2", "B3", "B4"],
                          ["C1", "C2", "C3", "C4"],
                          ["D1", "D2", "D3", "D4"]]

    @property
    def plateau(self):
        """
            PRE : -

            POST : Renvois la valeur de l'attribut self.__plateau qui est une liste de listes.

        """
        return self.__plateau


    @plateau.setter
    def plateau(self, value):
        """
            Cette fonction permet de modifier la valeur de l'attribut self.__plateau, principalement utilisé afin de
            reset le plateau entre deux partie.
            Cela permet de ne pas devoir relancer l'application.

            PRE : value est un "tableau" vide, une liste constituée de listes

            POST : change la valeur de l'attribut self.__plateau par la valeur placée en paramètre

        """
        self.__plateau = value


    @staticmethod
    def test_ligne(plateau_param):
        """Permet de tester si il y a une victoire sur une ligne.

            PRE : plateau_param est une list qui contient d'autres listes [[],[],[],[]]

            POST : renvois True si la longueur de chaque case d'une ligne est supérieur à 2 et si tout les cases possède
                   une valeur différente.

                   Exemple :
                   ["A1", "A2", "A3", "A4"] dans cette exemple toute les cases sont différentes mais on peut
                   constater que leur longueur est de 2 donc cela returnerai False

                   ["carre", "rond", "triangle", "croix"] dans cette exemple toute les cases sont différentes et on peut
                   constater que leur longueur est supérieur à 2 donc cela returnerai True
            RAISES : TypeError si type(plateau_param) != list

        """
        if type(plateau_param) != list:
            raise TypeError
        else:
            victoire = False
            for ligne in plateau_param:
                if (len(ligne[0]) > 2 and len(ligne[1]) > 2 and len(ligne[2]) > 2 and len(ligne[3]) > 2) and (
                        len(set(ligne)) == len(ligne)):
                    victoire = True
            return victoire


    def colonneVersLigne(self):
        """Permet de convertir les colonnes en lignes.

            PRE : -

            POST : Cette fonction va faire une transposition du plateau self.__plateau afin que par la suite on puisse
                   faire des testes sur les lignes via la fonction test_ligne().
                   Le plateau modifier "new_plateau_colonne" est renvoyé.

                   Exemple :
                   [["A1", "A2", "A3", "A4"],
                   ["B1", "B2", "B3", "B4"],
                   ["C1", "C2", "C3", "C4"],
                   ["D1", "D2", "D3", "D4"]]

                   Le plateau ci-dessus deviendrai ceci

                   [["A1", "B1", "C1", "D1"],
                   ["A2", "B2", "C2", "D2"],
                   ["A3", "B3", "C3", "D3"],
                   ["A4", "B4", "C4", "D4"]]

            RAISES : TypeError si Type(new_plateau_colonne) != list

        """
        new_plateau_colonne = [[], [], [], []]

        for i in self.__plateau:
            new_plateau_colonne[0].append(i[0])
            new_plateau_colonne[1].append(i[1])
            new_plateau_colonne[2].append(i[2])
            new_plateau_colonne[3].append(i[3])
        return new_plateau_colonne

    def zoneVersLigne(self):
        """Permet de convertir les zones en lignes.

            PRE : -

            POST : Cette fonction va faire une modification du plateau self.__plateau afin de convertir les zones du
                   plateau en ligne. Cela facilitera le test de victoire via la fonction test_ligne()
                   Le plateau modifier "new_plateau_zone" est renvoyé.

                   Exemple :
                   [["A1", "A2", "A3", "A4"],
                   ["B1", "B2", "B3", "B4"],
                   ["C1", "C2", "C3", "C4"],
                   ["D1", "D2", "D3", "D4"]]

                   Le plateau ci-dessus deviendrai ceci

                   [["A1", "A2", "B1", "B2"],
                   ["A3", "A4", "B3", "B4"],
                   ["C1", "C2", "D1", "D2"],
                   ["C3", "C4", "D3", "D4"]]

            RAISES : TypeError si Type(new_plateau_colonne) != list

        """
        new_plateau_zone = [[], [], [], []]
        demi_plateau1 = [self.__plateau[0], self.__plateau[1]]
        demi_plateau2 = [self.__plateau[2], self.__plateau[3]]

        for i in demi_plateau1:
            new_plateau_zone[0].append(i[0])
            new_plateau_zone[0].append(i[1])
            new_plateau_zone[1].append(i[2])
            new_plateau_zone[1].append(i[3])
        for i in demi_plateau2:
            new_plateau_zone[2].append(i[0])
            new_plateau_zone[2].append(i[1])
            new_plateau_zone[3].append(i[2])
            new_plateau_zone[3].append(i[3])

        return new_plateau_zone


    def testVictoire(self, joueur):
        """Test si il y a une victoire

            PRE : joueur == string qui correspond au pseudo du joueur

            POST : Cette fonction va renvoyé True si un des trois testes de victoire est validé.
                   Afin de tester la victoire, on utilise la fonction test_ligne() qui permet de tester la victoire sur
                   les lignes, colonneVersLigne() qui permet de transposer les colones en lignes et finalement
                   zoneVersLigne() qui permet de modifier les zones du plateau en lignes.

            RAISES : TypeError si Type(joueur) != str

        """
        if self.test_ligne(self.__plateau) or self.test_ligne(self.colonneVersLigne()) or self.test_ligne(
                self.zoneVersLigne()):
            print("Victoire, GG à " + joueur)
            return True

    def testEgualite(self):
        """
            Permet de tester si il y a une victoire sur une ligne.

            PRE : -

            POST : Cette fonction va renvoyer True si toutes les longueurs des cases du plateau est supérieur à 2.
                   Cela  signifie que le plateau est plein et qu'il n'y a eu aucune victoire.

            RAISES : -

        """
        for ligne in self.__plateau:
            for case in ligne:
                if len(case) == 2:
                    return False
        print("Egalité")
        return True
