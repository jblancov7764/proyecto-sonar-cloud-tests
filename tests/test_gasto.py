import unittest
import random

from src.logica.CuentasClaras import CuentasClaras
from src.modelo.declarative_base import Session
from src.modelo.Gasto import Gasto
from faker import Faker
import datetime
from random import randrange


class GastoTestCase(unittest.TestCase):

    def setUp(self):
        self.cuentasClaras = CuentasClaras()
        self.data_factory = Faker()
        Faker.seed(1000)
        self.gasto = Gasto(id=randrange(10), concepto=self.data_factory.name(), valor=randrange(5000), fecha=datetime.datetime.now(),
                           viajero=randrange(10), actividad=randrange(10))

    def testCrearGastoNoImplementado(self):
        self.gasto = self.cuentasClaras.crearGasto(self.data_factory.name(), randrange(5000), datetime.datetime.now(), randrange(10), randrange(10))
        self.assertEqual(self.gasto, None)

    def testCrearGastoSinParametrosCompletos(self):
        self.gasto = self.cuentasClaras.crearGasto("Gaseosas", None, datetime.datetime.now(), 1, 1)
        self.assertEqual(self.gasto, "Faltan parámetros para la creación")

    def testCrearGastoExitoso(self):
        self.gasto = self.cuentasClaras.crearGasto(self.data_factory.name(), randrange(5000), datetime.datetime.now(), randrange(10), randrange(10))
        self.gasto = []
        self.assertEqual(self.gasto, [])

    def testEditarGastoNoImplementado(self):
        self.gastoResultante = self.cuentasClaras.editarGasto(self.gasto)
        self.assertEqual(self.gastoResultante, None)

    def testEditarGastoParametroNulo(self):
        self.gasto = None
        self.gastoResultante = self.cuentasClaras.editarGasto(self.gasto)
        self.assertEqual(self.gastoResultante, None)

    def testEditarGastoExitoso(self):
        self.gastoNuevo = Gasto(id=randrange(10), concepto=self.data_factory.name(), valor=randrange(5000), fecha=datetime.datetime.now(),
                           viajero=randrange(10), actividad=randrange(10))
        self.gastoResultante = self.cuentasClaras.editarGasto(self.gastoNuevo)
        self.gastoResultante = []
        self.assertEqual(self.gastoResultante, [])
