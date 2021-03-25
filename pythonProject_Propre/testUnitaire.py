import unittest
from plateau.plateau import Plateau
from joueur.joueur import Joueur
from QuantikGame.partieGraphique import MenuHistorique
from QuantikGame.partieGraphique import MenuJouer
from partie.partieConsole import PartieConsole
from QuantikGame.partieGraphique import PartieGraphique

class TestQuantikGame(unittest.TestCase):


    def test_test_ligne(self):
        """vérification que la fonction test_ligne return bien True quand une ligne est gagnante"""
        plateau = Plateau()
        self.assertEqual(plateau.test_ligne([["A1", "A2", "A3", "A4"],
                                            ["B1", "B2", "B3", "B4"],
                                            ["C1", "C2", "C3", "C4"],
                                            ["D1", "D2", "D3", "D4"]]), False)

        self.assertEqual(plateau.test_ligne([["Carre", "Rond", "Croix", "Triangle"],
                                             ["B1", "B2", "B3", "B4"],
                                             ["C1", "C2", "C3", "C4"],
                                             ["D1", "D2", "D3", "D4"]]), True)

        self.assertEqual(plateau.test_ligne([["A1", "A2", "A3", "A4"],
                                             ["Carre", "Rond", "Croix", "Triangle"],
                                             ["C1", "C2", "C3", "C4"],
                                             ["D1", "D2", "D3", "D4"]]), True)

        self.assertEqual(plateau.test_ligne([["A1", "A2", "A3", "A4"],
                                             ["B1", "B2", "B3", "B4"],
                                             ["Carre", "Rond", "Croix", "Triangle"],
                                             ["D1", "D2", "D3", "D4"]]), True)

        self.assertEqual(plateau.test_ligne([["A1", "A2", "A3", "A4"],
                                             ["B1", "B2", "B3", "B4"],
                                             ["C1", "C2", "C3", "C4"],
                                             ["Carre", "Rond", "Croix", "Triangle"]]), True)

    def test_colonneVersLigne(self):
        """vérification que la fonction colonneVersLigne convertit bien les colonnes en lignes"""
        plateau = Plateau()
        reponse = [["A1", "B1", "C1", "D1"],
                   ["A2", "B2", "C2", "D2"],
                   ["A3", "B3", "C3", "D3"],
                   ["A4", "B4", "C4", "D4"]]
        self.assertEqual(plateau.colonneVersLigne(), reponse)

    def test_zoneVersLigne(self):
        """vérification que la fonction zoneVersLigne convertit bien les zone en lignes"""
        plateau = Plateau()
        reponse = [["A1", "A2", "B1", "B2"],
                   ["A3", "A4", "B3", "B4"],
                   ["C1", "C2", "D1", "D2"],
                   ["C3", "C4", "D3", "D4"]]
        self.assertEqual(plateau.zoneVersLigne(), reponse)

    def test_testVictoire(self):
        plateau = Plateau()
        """"Test de victoire sur une ligne"""
        plateau.plateau = [["Carre", "Rond", "Croix", "Triangle"],
                           ["B1", "B2", "B3", "B4"],
                           ["C1", "C2", "C3", "C4"],
                           ["D1", "D2", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)
        plateau.plateau = [["A1", "A2", "A3", "A4"],
                           ["B1", "B2", "B3", "B4"],
                           ["Carre", "Rond", "Croix", "Triangle"],
                           ["D1", "D2", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)
        plateau.plateau = [["A1", "A2", "A3", "A4"],
                           ["B1", "B2", "B3", "B4"],
                           ["C1", "C2", "C3", "C4"],
                           ["Carre", "Rond", "Croix", "Triangle"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        """"Test de victoire sur une colonne"""
        plateau.plateau = [["Carre", "A2", "B1", "B2"],
                           ["Rond", "A4", "B3", "B4"],
                           ["Triangle", "C2", "D1", "D2"],
                           ["Croix", "C4", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        plateau.plateau = [["A1", "A2", "B1", "Rond"],
                           ["A3", "A4", "B3", "Croix"],
                           ["C1", "C2", "D1", "Carre"],
                           ["C3", "C4", "D3", "Triangle"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        plateau.plateau = [["A1", "A2", "Triangle", "B2"],
                           ["A3", "A4", "Croix", "B4"],
                           ["C1", "C2", "Rond", "D2"],
                           ["C3", "C4", "Carre", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        """"Test de victoire sur une zone"""
        plateau.plateau = [["Carre", "Rond", "B1", "B2"],
                           ["Triangle", "Croix", "B3", "B4"],
                           ["C1", "C2", "D1", "D2"],
                           ["C3", "C4", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        plateau.plateau = [["A1", "A2", "B1", "B2"],
                           ["A3", "A4", "B3", "B4"],
                           ["C1", "C2", "Rond", "Carre"],
                           ["C3", "C4", "Croix", "Triangle"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        plateau.plateau = [["A1", "A2", "B1", "B2"],
                           ["A3", "A4", "B3", "B4"],
                           ["Carre", "Triangle", "D1", "D2"],
                           ["Croix", "Rond", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)


    def test_get_winrate(self):
        historique = MenuHistorique()
        valeur_param1 = [["Zaboudi", "Spearaw", 1, 12, "2020-12-02"], ["Zaboudi", "Spearaw", 2, 4, "2020-12-13"]]
        valeur_param2 = [["Zaboudi", "Spearaw", 2, 12, "2020-12-02"], ["Zaboudi", "Spearaw", 2, 4, "2020-12-13"]]
        valeur_param3 = [["Zaboudi", "Spearaw", 1, 12, "2020-12-02"], ["Zaboudi", "Spearaw", 2, 4, "2020-12-13"], ["Zaboudi", "Spearaw", 1, 8, "2020-12-02"]]

        self.assertEqual(historique.get_winrate(valeur_param1, "Zaboudi"), 50.00)
        self.assertEqual(historique.get_winrate(valeur_param1, "Spearaw"), 50.00)
        self.assertEqual(historique.get_winrate(valeur_param2, "Zaboudi"), 0.00)
        self.assertEqual(historique.get_winrate(valeur_param2, "Spearaw"), 100.00)
        self.assertEqual(historique.get_winrate(valeur_param3, "Zaboudi"), 66.67)
        self.assertEqual(historique.get_winrate(valeur_param3, "Spearaw"), 33.33)


    def test_testEgualite(self):
        """"Test si toute les cases ne sont pas égales à deux de longueur"""
        plateau = Plateau()
        plateau.plateau = [["Carre", "Carre", "Rond", "Rond"],
                           ["Carre", "Carre", "Rond", "Rond"],
                           ["Croix", "Croix", "Triangle", "Triangle"],
                           ["Croix", "Croix", "Triangle", "Triangle"]]
        self.assertEqual(plateau.testEgualite(), True)

        plateau.plateau = [["A1", "A2", "B1", "B2"],
                           ["A3", "A4", "B3", "B4"],
                           ["C1", "C2", "D1", "D2"],
                           ["C3", "C4", "D3", "D4"]]
        self.assertEqual(plateau.testEgualite(), False)
    
    def test_convertir_date(self):
        historique = MenuHistorique()
        valeur_param = ["2020-12-02", "2019-11-05", "2010-02-12", "2000-10-26"]
        reponse = ["02-12-2020", "05-11-2019", "12-02-2010", "26-10-2000"]
        self.assertEqual(historique.convertir_date(valeur_param[0]), reponse[0])
        self.assertEqual(historique.convertir_date(valeur_param[1]), reponse[1])
        self.assertEqual(historique.convertir_date(valeur_param[2]), reponse[2])
        self.assertEqual(historique.convertir_date(valeur_param[3]), reponse[3])

    def test_constructor_plateau(self):
        menu_plateau = Plateau()
        self.assertEqual(menu_plateau.plateau, [["A1", "A2", "A3", "A4"],["B1", "B2", "B3", "B4"],["C1", "C2", "C3", "C4"],["D1", "D2", "D3", "D4"]])

    def test_constructor_partie_console(self):
        partie_console = PartieConsole()
        self.assertEqual(type(partie_console.random), int)
        self.assertIsInstance(partie_console.plateau, Plateau)

    def test_constructor_joueur(self):
        joueur = Joueur("Test")
        self.assertEqual(joueur.pieces, {"carre": 2,"rond": 2,"triangle": 2,"croix": 2})
        self.assertEqual(joueur.pseudo, "Test")
        self.assertEqual(type(joueur.couleur), str)

    def test_constructor_partie_graphique(self):
        partie_graphique = PartieGraphique("pseudo1", "pseudo2")
        self.assertEqual(partie_graphique.joueur1, "pseudo1")
        self.assertEqual(partie_graphique.joueur2, "pseudo2")
        self.assertIsInstance(partie_graphique.plateau, Plateau)

if __name__ == '__main__':
    unittest.main()