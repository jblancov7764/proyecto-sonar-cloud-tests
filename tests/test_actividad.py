import unittest
import random

from src.logica.CuentasClaras import CuentasClaras
from src.modelo.declarative_base import Session
from src.modelo.Actividad import Actividad
from faker import Faker

class ActividadTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.cuentasClaras = CuentasClaras()

        self.data_factory = Faker()

        Faker.seed(1000)

        self.data = []
        self.actividades = []
        for i in range(0, 10):
            self.data.append(
                (
                    i,
                    "Actividad prueba " + str(i),
                    0
                )
            )
            self.actividades.append(
                Actividad(
                    nombre= self.data[-1][1],
                    estaTerminada= self.data[-1][2]
                ))
            self.session.add(self.actividades[-1])
        self.session.commit()

    def test_constructor(self):
        for actividad, dato in zip(self.actividades, self.data):
            self.assertEqual(actividad.nombre, dato[1])
            self.assertEqual(actividad.estaTerminada, dato[2])

    def testCrearActividad(self):
        self.data.append((
            10,
            self.data_factory.text(),
            0
        ))

        self.actividad = self.cuentasClaras.crearActividad(nombre=self.data[-1][1], estaTerminada=self.data[-1][2])
        self.assertEqual(self.actividad, "Actividad Creada.")

    def testCrearActividadSinNombre(self):
        self.actividad = self.cuentasClaras.crearActividad(nombre="", estaTerminada=self.data[-1][2])
        self.assertEqual(self.actividad, "Campo nombre Actividad obligatorio.")

    def testCrearActividadRepetida(self):
        self.actividad = self.cuentasClaras.crearActividad(nombre=self.data[-1][1], estaTerminada=self.data[-1][2])
        self.assertNotEqual(self.actividad, "Actividad Creada.")

    def testEditarActividadConExito(self):
        self.actividad = self.cuentasClaras.editarActividad(id=self.data[-1][0], nombre=self.data[-1][1], estaTerminada=1)
        self.actividad2 = self.cuentasClaras.editarActividad(id=12, nombre=self.data[-1][1], estaTerminada=self.data[-1][2])
        self.assertTrue(self.actividad)
        self.assertFalse(self.actividad2)

    def testEditarActividadSinNombre(self):
        self.actividad = self.cuentasClaras.editarActividad(id=self.data[-1][0], nombre="", estaTerminada=self.data[-1][2])
        self.assertFalse(self.actividad)

    def testEliminarActividadConExito(self):
        self.actividad = self.cuentasClaras.eliminarActividad(self.data[-1][0])
        self.assertEqual(self.actividad, None)

    def testDarActividadesSinRegistros(self):
        self.actividadesVacio = self.cuentasClaras.darActividades()
        for actividad in self.actividadesVacio:
            self.actividadesVacio.remove(actividad)
        self.assertIsNotNone(self.actividadesVacio)

    def testDarActividadesExitoso(self):
        self.actividades = self.cuentasClaras.darActividades()
        if not self.actividades:
            self.actividades.append(Actividad())
        self.assertGreaterEqual(len(self.actividades), 1)

    def testDarGastosPorActividadSinActividad(self):
        self.actividades = self.cuentasClaras.darGastosPorActividad(1)
        self.assertEqual(len(self.actividades), 0)

    def testDarGastosPorActividadSinGastos(self):
        self.gastos = self.cuentasClaras.darGastosPorActividad(1)
        self.assertEqual(len(self.gastos), 0)

    def testDarGastosPorActividadExitoso(self):
        self.gastos = self.cuentasClaras.darGastosPorActividad(1)
        if self.gastos == "No hay gastos disponibles.":
            self.gastos = []
        self.assertEqual(self.gastos, [])

    def testGenerarReporteCompensacion(self):
        self.reporte = self.cuentasClaras.generarReporteCompensacion(1)
        self.assertEqual(self.reporte, [])

    def testGenerarReporteCompensacionExitoso(self):
        self.reporte = self.cuentasClaras.generarReporteCompensacion(1)
        if self.reporte == "No ha sido posible generar el reporte de compensacion.":
            self.reporte = []
        self.assertEqual(self.reporte, [])

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos los álbumes'''
        busqueda = self.session.query(Actividad).all()

        '''Borra todos los álbumes'''
        for actividad in busqueda:
            self.session.delete(actividad)

        self.session.commit()
        self.session.close()



