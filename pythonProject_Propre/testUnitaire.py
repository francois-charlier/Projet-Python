import unittest
from plateau.plateau import Plateau
from joueur.joueur import Joueur
from QuantikGame.partieGraphique import MenuHistorique
from QuantikGame.partieGraphique import MenuJouer
from partie.partieConsole import PartieConsole

class TestQuantikGame(unittest.TestCase):

    def test_instance_plateau(self):
        plateau = Plateau()
        self.assertIsInstance(plateau, Plateau)

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

        """"Test de victoire sur une colonne"""
        plateau.plateau = [["Carre", "A2", "B1", "B2"],
                           ["Rond", "A4", "B3", "B4"],
                           ["Triangle", "C2", "D1", "D2"],
                           ["Croix", "C4", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

        """"Test de victoire sur une zone"""
        plateau.plateau = [["Carre", "Rond", "B1", "B2"],
                           ["Triangle", "Croix", "B3", "B4"],
                           ["C1", "C2", "D1", "D2"],
                           ["C3", "C4", "D3", "D4"]]
        self.assertEqual(plateau.testVictoire("Pseudo"), True)

    def test_instance_joueur(self):
        joueur = Joueur("Pseudo")
        self.assertIsInstance(joueur, Joueur)

    def test_get_winrate(self):
        historique = MenuHistorique()
        valeur_param = [["Zaboudi", "Spearaw", 1, 12, "2020-12-02"], ["Zaboudi", "Spearaw", 2, 4, "2020-12-13"]]
        self.assertEqual(historique.get_winrate(valeur_param, "Zaboudi"), 50.00)

    def test_instance_partie_console(self):
        partie_console = PartieConsole()
        self.assertIsInstance(partie_console, PartieConsole)
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
        valeur_param = "2020-12-02"
        reponse = "02-12-2020"
        self.assertEqual(historique.convertir_date(valeur_param), reponse)

    def test_instance_menu_jouer(self):
        menu_jouer = MenuJouer()
        self.assertIsInstance(menu_jouer, MenuJouer)

    def test_instance_menu_historique(self):
        menu_historique = MenuHistorique()
        self.assertIsInstance(menu_historique, MenuHistorique)


if __name__ == '__main__':
    unittest.main()