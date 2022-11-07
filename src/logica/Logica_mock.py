'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.CuentasClaras import CuentasClaras


class Logica_mock():

    def __init__(self):
        self.cuentasClaras = CuentasClaras()
        # Este constructor contiene los datos falsos para probar la interfaz
        self.actividades = self.cuentasClaras.darActividades()
