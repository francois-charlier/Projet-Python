class Plateau:

    # Definition du plateau du jeu
    def __init__(self):
        self.__plateau = [["A1", "A2", "A3", "A4"],
                          ["B1", "B2", "B3", "B4"],
                          ["C1", "C2", "C3", "C4"],
                          ["D1", "D2", "D3", "D4"]]

    @property
    def plateau(self):
        return self.__plateau


    @plateau.setter
    def plateau(self, value):
        self.__plateau = value


    @staticmethod
    def test_ligne(plateau_param):
        """Permet de tester si il y a une victoire sur une ligne.

            PRE : plateau_param == list de list
            POST : renvois True si len(ligne[0]) > 2 et len(ligne[1]) > 2 et len(ligne[2]) > 2 et len(ligne[3]) > 2) et
                    len(set(ligne)) == len(ligne), renvois False si une ou plusieurs conditions n'est pas respecté(es)
            RAISES : TypeError si type(plateau_param) != list

        """
        if type(plateau_param) != list:
            raise TypeError
        else:
            try:
                victoire = False
                for ligne in plateau_param:
                    if (len(ligne[0]) > 2 and len(ligne[1]) > 2 and len(ligne[2]) > 2 and len(ligne[3]) > 2) and (
                            len(set(ligne)) == len(ligne)):
                        victoire = True
            except TypeError:
                print("Mauvais type")
            return victoire


    def colonneVersLigne(self):
        """Permet de convertir les colonnes en lignes.

            PRE : -
            POST : renvoie new_plateau_colonne qui est une modification de self.__plateau (transposer)
            RAISES : TypeError si Type(new_plateau_colonne) != list

        """
        new_plateau_colonne = [[], [], [], []]
        if type(self.__plateau) != list:
            raise TypeError
        try:
            for i in self.__plateau:
                new_plateau_colonne[0].append(i[0])
                new_plateau_colonne[1].append(i[1])
                new_plateau_colonne[2].append(i[2])
                new_plateau_colonne[3].append(i[3])
        except TypeError:
          print("Mauvais type")
        return new_plateau_colonne

    def zoneVersLigne(self):
        """Permet de convertir les zones en lignes.

            PRE : -
            POST : renvoie new_plateau_zone qui est une modification de self.__plateau
            RAISES : TypeError si Type(new_plateau_colonne) != list

        """
        new_plateau_zone = [[], [], [], []]
        demi_plateau1 = [self.__plateau[0], self.__plateau[1]]
        demi_plateau2 = [self.__plateau[2], self.__plateau[3]]
        if type(new_plateau_zone) != list:
            raise TypeError
        try:
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
        except TypeError:
            print("Mauvais Type")
        return new_plateau_zone


    def testVictoire(self, joueur):
        """Test si il y a une victoire

            PRE : joueur == string qui correspond au pseudo du joueur
            POST : Renvoie True si self.test_ligne(self.__plateau) ou self.test_ligne(self.colonneVersLigne()) ou self.test_ligne(
                self.zoneVersLigne()
            RAISES : TypeError si Type(joueur) != str

        """
        if type(joueur) != str:
            raise TypeError

        if self.test_ligne(self.__plateau) or self.test_ligne(self.colonneVersLigne()) or self.test_ligne(
                self.zoneVersLigne()):
            print("Victoire, GG à " + joueur)
            return True

    def testEgualite(self):
        """Permet de tester si il y a une victoire sur une ligne.

            PRE : -
            POST : Renvoie True si toutes les longueurs d'élément sont égales à deux et False dans le cas contraire.
            RAISES : -

        """
        for ligne in self.__plateau:
            for case in ligne:
                if len(case) == 2:
                    return False
        print("Egalité")
        return True
