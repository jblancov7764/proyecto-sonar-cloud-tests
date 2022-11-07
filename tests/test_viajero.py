import unittest
import random

from src.logica.CuentasClaras import CuentasClaras
from src.modelo.declarative_base import Session
from src.modelo.Viajero import Viajero
from faker import Faker

class ViajeroTestCase(unittest.TestCase):

    def setUp(self):
        self.cuentasClaras = CuentasClaras()
        self.session = Session()
        self.data_factory = Faker()

        Faker.seed(1000)

        self.data = []
        self.viajeros = []

        for i in range(0, 10):
            self.data.append(
                (
                    i,
                    self.data_factory.name(),
                    self.data_factory.last_name()
                )
            )
            self.viajeros.append(
                Viajero(
                    nombre=self.data[-1][1],
                    apellido=self.data[-1][2]
            ))
            self.session.add(self.viajeros[-1])
        self.session.commit()

    def test_constructor(self):
        for viajero, dato in zip(self.viajeros, self.data):
            self.assertEqual(viajero.nombre, dato[1])
            self.assertEqual(viajero.apellido, dato[2])

    def testCrearViajero(self):
        self.data.append((
            10,
            self.data_factory.name(),
            self.data_factory.last_name()
        ))
        self.viajero = self.cuentasClaras.crearViajero(nombre=self.data[-1][1], apellido=self.data[-1][2])
        self.assertEqual(self.viajero, "Viajero Creado.")

    def testCrearViajeroSinNombre(self):
        self.viajero = self.cuentasClaras.crearViajero(nombre="", apellido=self.data[-1][2])
        self.assertEqual(self.viajero, "Campo Nombre Viajero es obligatorio.")

    def testCrearViajeroSinApellido(self):
        self.viajero = self.cuentasClaras.crearViajero(nombre=self.data[-1][1], apellido=None)
        self.assertEqual(self.viajero, "Campo Apellido Viajero es obligatorio.")

    def testCrearViajeroRepetido(self):
        self.viajero = self.cuentasClaras.crearViajero(nombre=self.data[-1][1], apellido=self.data[-1][2])
        self.assertNotEqual(self.viajero,"Viajero Creado.")

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos los viajeros'''
        busqueda = self.session.query(Viajero).all()

        '''Borra todos los viajeros'''
        for viajero in busqueda:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()


if __name__ == '__main__':
    unittest.main()
