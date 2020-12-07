# Il s'agit de la class plateau qui stocke le plateau au fur et à mesure de la partie.
# C'est également celle-ci qui va vérifier après chaque les conditions de victoire et annoncer le vainqueur
# s'il y en a un.
#
#  Francois Charlier

class Plateau():

# Definition du plateau du jeu
    def __init__(self):
        self.__plateau = [["A1","A2","A3","A4"],
                          ["B1","B2","B3","B4"],
                          ["C1","C2","C3","C4"],
                          ["D1","D2","D3","D4"]]

    @property
    def plateau(self):
        return self.__plateau

# Permet de tester si il y a une victoire sur une ligne.

    def testLigne(self, plateau_param):
        victoire = False
        for ligne in plateau_param:
            if (len(ligne[0]) > 2 and len(ligne[1]) > 2 and len(ligne[2]) > 2 and len(ligne[3]) > 2) and (len(set(ligne)) == len(ligne)):
                victoire = True
        return victoire

# Permet de convertir les colonnes en lignes.
    def colonneVersLigne(self):
        new_plateau_colonne = [[], [], [], []]
        for i in self.__plateau:
            new_plateau_colonne[0].append(i[0])
            new_plateau_colonne[1].append(i[1])
            new_plateau_colonne[2].append(i[2])
            new_plateau_colonne[3].append(i[3])

        return new_plateau_colonne

# Permet de convertir les zones en lignes.
    def zoneVersLigne(self):
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

# Test si il y a une victoire
    def testVictoire(self, joueur):
        if self.testLigne(self.__plateau) or self.testLigne(self.colonneVersLigne()) or self.testLigne(self.zoneVersLigne()):
            print("Victoire, GG à " + joueur)
            return True