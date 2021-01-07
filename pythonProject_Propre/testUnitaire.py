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


if __name__ == '__main__':
    unittest.main()