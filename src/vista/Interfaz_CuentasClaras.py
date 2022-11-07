from PyQt5.QtWidgets import QApplication
from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero
from src.logica.CuentasClaras import CuentasClaras
from datetime import datetime


class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)

        self.logica = logica
        self.mostrar_vista_lista_actividades()
        self.cuentasClaras = CuentasClaras()
        self.actividad_seleccionada = None
        self.id_actividad_seleccionada = None

    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """
        self.vista_lista_actividades = Vista_lista_actividades(self)
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def editar_actividad(self, indice_actividad, nombre):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        for indice in range(len(self.logica.actividades)):
            actividad = self.logica.actividades[indice]
            if actividad.id == indice_actividad:
                self.logica.actividades[indice].nombre = nombre
                break
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def eliminar_actividad(self, indice_actividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.cuentasClaras.eliminarActividad(indice_actividad)
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """
        self.vista_lista_viajeros = Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.cuentasClaras.darViajeros())

    def insertar_viajero(self, nombre, apellido):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.cuentasClaras.crearViajero(nombre, apellido)
        self.vista_lista_viajeros.mostrar_viajeros(self.cuentasClaras.darViajeros())

    def editar_viajero(self, indice_viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros[indice_viajero] = {"Nombre": nombre, "Apellido": apellido}
        self.vista_lista_viajeros.mostrar_viajeros(self.cuentasClaras.darViajeros())

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.cuentasClaras.darViajeros())

    def mostrar_actividad(self, id_actividad):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        for indice in range(len(self.logica.actividades)):
            self.actividad_seleccionada = self.logica.actividades[indice]
            if self.actividad_seleccionada.id == id_actividad:
                self.id_actividad_seleccionada = id_actividad
                break
        self.vista_actividad = Vista_actividad(self)
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_seleccionada,
                                                          self.cuentasClaras.darGastosPorActividad(id_actividad))

    def insertar_gasto(self, concepto, fecha, valor):
        """
        Esta función inserta un gasto a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.cuentasClaras.crearGasto(concepto, valor, fecha, None, self.id_actividad_seleccionada)
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_seleccionada,
                                                          self.cuentasClaras.darGastosPorActividad(
                                                              self.id_actividad_seleccionada))

    def editar_gasto(self, gasto, concepto, fecha, valor):
        """
        Esta función edita un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        gasto.concepto = concepto
        gasto.fecha = datetime.strptime(fecha, '%d/%m/%Y')
        gasto.valor = valor
        self.cuentasClaras.editarGasto(gasto)
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_seleccionada,
                                                          self.cuentasClaras.darGastosPorActividad(
                                                              self.id_actividad_seleccionada))

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividad_seleccionada,
                                                          self.cuentasClaras.darGastosPorActividad(
                                                              self.id_actividad_seleccionada))

    def mostrar_reporte_compensacion(self):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        self.vista_reporte_comensacion = Vista_reporte_compensacion(self)
        self.vista_reporte_comensacion.id_actividad = self.actividad_seleccionada.id
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(self.cuentasClaras.generarReporteCompensacion(self.id_actividad_seleccionada))

    def mostrar_reporte_gastos_viajero(self, id_actividad):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self)
        self.vista_reporte_gastos.mostar_reporte_gastos(self.cuentasClaras.verGastosViajeroPorActividad(id_actividad),
                                                        id_actividad)

    def actualizar_viajeros(self, n_viajeros_en_actividad):
        """
        Esta función añade un viajero a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros_en_actividad = n_viajeros_en_actividad

    def dar_viajeros(self, id_actividad):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        return self.cuentasClaras.darViajerosAsociadosEnActividad(id_actividad)

    def dar_viajeros_en_actividad(self, id_actividad):
        """
        Esta función pasa los viajeros de una actividad (debe implementarse como una lista de diccionarios o str)
        """
        return self.cuentasClaras.darViajerosPorActividad(id_actividad)

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass
