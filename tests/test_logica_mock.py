import unittest
from src.logica.Logica_mock import Logica_mock


class LogicaMockTestCase(unittest.TestCase):

    def testInstanciarLogicaExitoso(self):
        self.logicaMock = Logica_mock()
        self.assertNotEqual(self.logicaMock, None)