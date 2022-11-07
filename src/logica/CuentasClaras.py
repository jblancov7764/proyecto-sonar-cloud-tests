from src.modelo.Actividad import Actividad, ViajeroActividad
from src.modelo.Viajero import Viajero
from src.modelo.Gasto import Gasto
from src.modelo.declarative_base import engine, Base, session
from datetime import datetime


class CuentasClaras():

    def __init__(self):
        Base.metadata.create_all(engine)

    def crearActividad(self, nombre, estaTerminada):
        self.actividad = Actividad(nombre=nombre, estaTerminada=estaTerminada)
        self.act = session.query(Actividad).filter_by(nombre=nombre).first()
        if not nombre or nombre.isspace():
            return "Campo nombre Actividad obligatorio."
        if self.act is not None:
            return "La actividad ya existe."
        session.add(self.actividad)
        session.commit()
        return "Actividad Creada."

    def editarActividad(self, id, nombre, estaTerminada):
        if not nombre or nombre.isspace():
            return False
        self.actividad = session.query(Actividad).filter(Actividad.id == id).first()
        if self.actividad is not None:
            self.actividad.nombre = nombre
            self.actividad.estaTerminada = estaTerminada
            session.commit()
            return True
        else:
            return False

    def editarActivity(self, id, nombre, estaTerminada):
        if not nombre or nombre.isspace():
            return False
        self.actividad = session.query(Actividad).filter(Actividad.id == id).first()
        if self.actividad is not None:
            self.actividad.nombre = nombre
            self.actividad.estaTerminada = estaTerminada
            session.commit()
            return True
        else:
            return False

    def eliminarActividad(self, id_actividad):
        session.query(Gasto).filter(Gasto.actividad == id_actividad).delete()
        session.query(ViajeroActividad).filter(ViajeroActividad.actividad_id == id_actividad).delete()
        session.query(Actividad).filter(Actividad.id == id_actividad).delete()
        session.commit()

    def borrarActividad(self, id_actividad):
        session.query(Gasto).filter(Gasto.actividad == id_actividad).delete()
        session.query(ViajeroActividad).filter(ViajeroActividad.actividad_id == id_actividad).delete()
        session.query(Actividad).filter(Actividad.id == id_actividad).delete()
        session.commit()

    def crearViajero(self, nombre, apellido):
        if not nombre or nombre.isspace():
            return "Campo Nombre Viajero es obligatorio."
        if not apellido or apellido.isspace():
            return "Campo Apellido Viajero es obligatorio."
        viajNombre = session.query(Viajero).filter(
            Viajero.nombre == nombre and Viajero.apellido == apellido).first()
        if viajNombre is not None:
            return "El viajero existe."
        viajero = Viajero(nombre=nombre, apellido=apellido)
        session.add(viajero)
        session.commit()
        return "Viajero Creado."

    def darActividades(self):
        self.actividades = session.query(Actividad).all()
        if len(self.actividades) == 0:
            return []
        else:
            return self.actividades

    def darGastosPorActividad(self, actividad_id):
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad_id).all()
        if len(gastos) > 0:
            return gastos
        else:
            return []

    def generarReporteCompensacion(self, actividad_id):
        reporte = []
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad_id).all()
        if len(gastos) > 0:
            totalGastos = 0
            for gasto in gastos:
                totalGastos += gasto.valor
            viajeros_actividades = session.query(ViajeroActividad).filter(
                ViajeroActividad.actividad_id == actividad_id).all()
            if len(viajeros_actividades) > 0:
                viajeros = []
                for viajero_actividad in viajeros_actividades:
                    viajeros.append(session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).first())
                totalPorPersona = totalGastos / len(viajeros)
                arr_les_deben = []
                arr_deben_pagar = []
                deuda_total = 0
                encabezado_index = []
                for viajero in viajeros:
                    encabezado_index.append(viajero.id)
                    gastos_por_viajero = list(filter(lambda gasto: gasto.viajero == viajero.id, gastos))
                    total_pagado_por_viajero = 0
                    for gasto_x_viajero in gastos_por_viajero:
                        total_pagado_por_viajero += gasto_x_viajero.valor
                    if total_pagado_por_viajero > totalPorPersona:
                        arr_les_deben.append({'id': viajero.id, 'valor': total_pagado_por_viajero - totalPorPersona,
                                              'nombre': viajero.nombre, 'apellido': viajero.apellido})
                    elif total_pagado_por_viajero < totalPorPersona:
                        arr_deben_pagar.append({'id': viajero.id, 'valor': totalPorPersona - total_pagado_por_viajero,
                                                'nombre': viajero.nombre, 'apellido': viajero.apellido, 'beneficiados': []})
                        deuda_total += totalPorPersona - total_pagado_por_viajero
                while deuda_total > 0:
                    for viajero_le_deben in arr_les_deben:
                        if viajero_le_deben['valor'] > 0:
                            for viajero_debe_pagar in arr_deben_pagar:
                                if viajero_debe_pagar['valor'] > 0:
                                    if viajero_le_deben['valor'] >= viajero_debe_pagar['valor']:
                                        viajero_le_deben['valor'] -= viajero_debe_pagar['valor']
                                        deuda_total -= viajero_debe_pagar['valor']
                                        viajero_debe_pagar['beneficiados'].append({'id': viajero_le_deben['id'], 'valor': viajero_debe_pagar['valor']})
                                        viajero_debe_pagar['valor'] = 0
                                    else:
                                        viajero_debe_pagar['valor'] -= viajero_le_deben['valor']
                                        deuda_total -= viajero_le_deben['valor']
                                        viajero_debe_pagar['beneficiados'].append(
                                            {'id': viajero_le_deben['id'], 'valor': viajero_le_deben['valor']})
                                        viajero_le_deben['valor'] = 0
                                        break
                    if deuda_total < 0.5:
                        deuda_total = 0
                encabezado = ['']
                for viajero in viajeros:
                    cuerpo_tabla = []
                    encabezado.append(viajero.nombre + ' ' + viajero.apellido)
                    cuerpo_tabla.append(viajero.nombre + ' ' + viajero.apellido)
                    viajero_tmp = None
                    for viajero_debe_pagar in arr_deben_pagar:
                        if viajero_debe_pagar['id'] == viajero.id:
                            viajero_tmp = viajero_debe_pagar
                            break
                    for id_index in encabezado_index:
                        if id_index == viajero.id:
                            cuerpo_tabla.append(-1)
                        else:
                            if viajero_tmp is not None:
                                encontro = False
                                for beneficiado in viajero_tmp['beneficiados']:
                                    if id_index == beneficiado['id']:
                                        encontro = True
                                        cuerpo_tabla.append(beneficiado['valor'])
                                        break
                                if not encontro:
                                    cuerpo_tabla.append(0)
                            else:
                                cuerpo_tabla.append(0)
                    reporte.append(cuerpo_tabla)
                reporte.insert(0, encabezado)
        return reporte

    def generarReportCompensacion(self, actividad_id):
        reporte = []
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad_id).all()
        if len(gastos) > 0:
            totalGastos = 0
            for gasto in gastos:
                totalGastos += gasto.valor
            viajeros_actividades = session.query(ViajeroActividad).filter(
                ViajeroActividad.actividad_id == actividad_id).all()
            if len(viajeros_actividades) > 0:
                viajeros = []
                for viajero_actividad in viajeros_actividades:
                    viajeros.append(session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).first())
                totalPorPersona = totalGastos / len(viajeros)
                arr_les_deben = []
                arr_deben_pagar = []
                deuda_total = 0
                encabezado_index = []
                for viajero in viajeros:
                    encabezado_index.append(viajero.id)
                    gastos_por_viajero = list(filter(lambda gasto: gasto.viajero == viajero.id, gastos))
                    total_pagado_por_viajero = 0
                    for gasto_x_viajero in gastos_por_viajero:
                        total_pagado_por_viajero += gasto_x_viajero.valor
                    if total_pagado_por_viajero > totalPorPersona:
                        arr_les_deben.append({'id': viajero.id, 'valor': total_pagado_por_viajero - totalPorPersona,
                                              'nombre': viajero.nombre, 'apellido': viajero.apellido})
                    elif total_pagado_por_viajero < totalPorPersona:
                        arr_deben_pagar.append({'id': viajero.id, 'valor': totalPorPersona - total_pagado_por_viajero,
                                                'nombre': viajero.nombre, 'apellido': viajero.apellido, 'beneficiados': []})
                        deuda_total += totalPorPersona - total_pagado_por_viajero
                while deuda_total > 0:
                    for viajero_le_deben in arr_les_deben:
                        if viajero_le_deben['valor'] > 0:
                            for viajero_debe_pagar in arr_deben_pagar:
                                if viajero_debe_pagar['valor'] > 0:
                                    if viajero_le_deben['valor'] >= viajero_debe_pagar['valor']:
                                        viajero_le_deben['valor'] -= viajero_debe_pagar['valor']
                                        deuda_total -= viajero_debe_pagar['valor']
                                        viajero_debe_pagar['beneficiados'].append({'id': viajero_le_deben['id'], 'valor': viajero_debe_pagar['valor']})
                                        viajero_debe_pagar['valor'] = 0
                                    else:
                                        viajero_debe_pagar['valor'] -= viajero_le_deben['valor']
                                        deuda_total -= viajero_le_deben['valor']
                                        viajero_debe_pagar['beneficiados'].append(
                                            {'id': viajero_le_deben['id'], 'valor': viajero_le_deben['valor']})
                                        viajero_le_deben['valor'] = 0
                                        break
                    if deuda_total < 0.5:
                        deuda_total = 0
                encabezado = ['']
                for viajero in viajeros:
                    cuerpo_tabla = []
                    encabezado.append(viajero.nombre + ' ' + viajero.apellido)
                    cuerpo_tabla.append(viajero.nombre + ' ' + viajero.apellido)
                    viajero_tmp = None
                    for viajero_debe_pagar in arr_deben_pagar:
                        if viajero_debe_pagar['id'] == viajero.id:
                            viajero_tmp = viajero_debe_pagar
                            break
                    for id_index in encabezado_index:
                        if id_index == viajero.id:
                            cuerpo_tabla.append(-1)
                        else:
                            if viajero_tmp is not None:
                                encontro = False
                                for beneficiado in viajero_tmp['beneficiados']:
                                    if id_index == beneficiado['id']:
                                        encontro = True
                                        cuerpo_tabla.append(beneficiado['valor'])
                                        break
                                if not encontro:
                                    cuerpo_tabla.append(0)
                            else:
                                cuerpo_tabla.append(0)
                    reporte.append(cuerpo_tabla)
                reporte.insert(0, encabezado)
        return reporte

    def generateReporteCompensacion(self, actividad_id):
        reporte = []
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad_id).all()
        if len(gastos) > 0:
            totalGastos = 0
            for gasto in gastos:
                totalGastos += gasto.valor
            viajeros_actividades = session.query(ViajeroActividad).filter(
                ViajeroActividad.actividad_id == actividad_id).all()
            if len(viajeros_actividades) > 0:
                viajeros = []
                for viajero_actividad in viajeros_actividades:
                    viajeros.append(session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).first())
                totalPorPersona = totalGastos / len(viajeros)
                arr_les_deben = []
                arr_deben_pagar = []
                deuda_total = 0
                encabezado_index = []
                for viajero in viajeros:
                    encabezado_index.append(viajero.id)
                    gastos_por_viajero = list(filter(lambda gasto: gasto.viajero == viajero.id, gastos))
                    total_pagado_por_viajero = 0
                    for gasto_x_viajero in gastos_por_viajero:
                        total_pagado_por_viajero += gasto_x_viajero.valor
                    if total_pagado_por_viajero > totalPorPersona:
                        arr_les_deben.append({'id': viajero.id, 'valor': total_pagado_por_viajero - totalPorPersona,
                                              'nombre': viajero.nombre, 'apellido': viajero.apellido})
                    elif total_pagado_por_viajero < totalPorPersona:
                        arr_deben_pagar.append({'id': viajero.id, 'valor': totalPorPersona - total_pagado_por_viajero,
                                                'nombre': viajero.nombre, 'apellido': viajero.apellido, 'beneficiados': []})
                        deuda_total += totalPorPersona - total_pagado_por_viajero
                while deuda_total > 0:
                    for viajero_le_deben in arr_les_deben:
                        if viajero_le_deben['valor'] > 0:
                            for viajero_debe_pagar in arr_deben_pagar:
                                if viajero_debe_pagar['valor'] > 0:
                                    if viajero_le_deben['valor'] >= viajero_debe_pagar['valor']:
                                        viajero_le_deben['valor'] -= viajero_debe_pagar['valor']
                                        deuda_total -= viajero_debe_pagar['valor']
                                        viajero_debe_pagar['beneficiados'].append({'id': viajero_le_deben['id'], 'valor': viajero_debe_pagar['valor']})
                                        viajero_debe_pagar['valor'] = 0
                                    else:
                                        viajero_debe_pagar['valor'] -= viajero_le_deben['valor']
                                        deuda_total -= viajero_le_deben['valor']
                                        viajero_debe_pagar['beneficiados'].append(
                                            {'id': viajero_le_deben['id'], 'valor': viajero_le_deben['valor']})
                                        viajero_le_deben['valor'] = 0
                                        break
                    if deuda_total < 0.5:
                        deuda_total = 0
                encabezado = ['']
                for viajero in viajeros:
                    cuerpo_tabla = []
                    encabezado.append(viajero.nombre + ' ' + viajero.apellido)
                    cuerpo_tabla.append(viajero.nombre + ' ' + viajero.apellido)
                    viajero_tmp = None
                    for viajero_debe_pagar in arr_deben_pagar:
                        if viajero_debe_pagar['id'] == viajero.id:
                            viajero_tmp = viajero_debe_pagar
                            break
                    for id_index in encabezado_index:
                        if id_index == viajero.id:
                            cuerpo_tabla.append(-1)
                        else:
                            if viajero_tmp is not None:
                                encontro = False
                                for beneficiado in viajero_tmp['beneficiados']:
                                    if id_index == beneficiado['id']:
                                        encontro = True
                                        cuerpo_tabla.append(beneficiado['valor'])
                                        break
                                if not encontro:
                                    cuerpo_tabla.append(0)
                            else:
                                cuerpo_tabla.append(0)
                    reporte.append(cuerpo_tabla)
                reporte.insert(0, encabezado)
        return reporte

    def generarReporteCompensation(self, actividad_id):
        reporte = []
        gastos = session.query(Gasto).filter(Gasto.actividad == actividad_id).all()
        if len(gastos) > 0:
            totalGastos = 0
            for gasto in gastos:
                totalGastos += gasto.valor
            viajeros_actividades = session.query(ViajeroActividad).filter(
                ViajeroActividad.actividad_id == actividad_id).all()
            if len(viajeros_actividades) > 0:
                viajeros = []
                for viajero_actividad in viajeros_actividades:
                    viajeros.append(session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).first())
                totalPorPersona = totalGastos / len(viajeros)
                arr_les_deben = []
                arr_deben_pagar = []
                deuda_total = 0
                encabezado_index = []
                for viajero in viajeros:
                    encabezado_index.append(viajero.id)
                    gastos_por_viajero = list(filter(lambda gasto: gasto.viajero == viajero.id, gastos))
                    total_pagado_por_viajero = 0
                    for gasto_x_viajero in gastos_por_viajero:
                        total_pagado_por_viajero += gasto_x_viajero.valor
                    if total_pagado_por_viajero > totalPorPersona:
                        arr_les_deben.append({'id': viajero.id, 'valor': total_pagado_por_viajero - totalPorPersona,
                                              'nombre': viajero.nombre, 'apellido': viajero.apellido})
                    elif total_pagado_por_viajero < totalPorPersona:
                        arr_deben_pagar.append({'id': viajero.id, 'valor': totalPorPersona - total_pagado_por_viajero,
                                                'nombre': viajero.nombre, 'apellido': viajero.apellido, 'beneficiados': []})
                        deuda_total += totalPorPersona - total_pagado_por_viajero
                while deuda_total > 0:
                    for viajero_le_deben in arr_les_deben:
                        if viajero_le_deben['valor'] > 0:
                            for viajero_debe_pagar in arr_deben_pagar:
                                if viajero_debe_pagar['valor'] > 0:
                                    if viajero_le_deben['valor'] >= viajero_debe_pagar['valor']:
                                        viajero_le_deben['valor'] -= viajero_debe_pagar['valor']
                                        deuda_total -= viajero_debe_pagar['valor']
                                        viajero_debe_pagar['beneficiados'].append({'id': viajero_le_deben['id'], 'valor': viajero_debe_pagar['valor']})
                                        viajero_debe_pagar['valor'] = 0
                                    else:
                                        viajero_debe_pagar['valor'] -= viajero_le_deben['valor']
                                        deuda_total -= viajero_le_deben['valor']
                                        viajero_debe_pagar['beneficiados'].append(
                                            {'id': viajero_le_deben['id'], 'valor': viajero_le_deben['valor']})
                                        viajero_le_deben['valor'] = 0
                                        break
                    if deuda_total < 0.5:
                        deuda_total = 0
                encabezado = ['']
                for viajero in viajeros:
                    cuerpo_tabla = []
                    encabezado.append(viajero.nombre + ' ' + viajero.apellido)
                    cuerpo_tabla.append(viajero.nombre + ' ' + viajero.apellido)
                    viajero_tmp = None
                    for viajero_debe_pagar in arr_deben_pagar:
                        if viajero_debe_pagar['id'] == viajero.id:
                            viajero_tmp = viajero_debe_pagar
                            break
                    for id_index in encabezado_index:
                        if id_index == viajero.id:
                            cuerpo_tabla.append(-1)
                        else:
                            if viajero_tmp is not None:
                                encontro = False
                                for beneficiado in viajero_tmp['beneficiados']:
                                    if id_index == beneficiado['id']:
                                        encontro = True
                                        cuerpo_tabla.append(beneficiado['valor'])
                                        break
                                if not encontro:
                                    cuerpo_tabla.append(0)
                            else:
                                cuerpo_tabla.append(0)
                    reporte.append(cuerpo_tabla)
                reporte.insert(0, encabezado)
        return reporte

    def crearGasto(self, concepto, valor, fecha, id_viajero, id_actividad):
        if concepto is None or valor is None or fecha is None or id_viajero is None or id_actividad is None:
            return "Faltan parámetros para la creación"
        self.actividad = session.query(Actividad).get(id_actividad)
        if self.actividad is not None:
            self.viajero = session.query(Viajero).get(id_viajero)
            if self.viajero is not None:
                self.gasto = Gasto(concepto=concepto, valor=valor, fecha=datetime.strptime(fecha, '%d/%m/%Y'),
                                   viajero=id_viajero,
                                   actividad=id_actividad)
                session.add(self.gasto)
                session.commit()
                return self.viajero
        return None

    def editarGasto(self, gasto):
        if gasto is None:
            return None
        self.gastoUpdate = session.query(Gasto).get(gasto.id)
        if self.gastoUpdate is not None:
            self.gastoUpdate.concepto = gasto.concepto
            self.gastoUpdate.valor = gasto.valor
            self.gastoUpdate.fecha = gasto.fecha
            session.commit()
            return self.gastoUpdate
        return None

    def asociarViajeroEnActividad(self, viajeros, id_actividad):
        actividad = session.query(Actividad).get(id_actividad)
        if actividad is None:
            return "No existe la actividad solicitada."
        for viajero in viajeros:
            if viajero.presente:
                viajero_act_temp = session.query(ViajeroActividad).filter(
                    ViajeroActividad.viajero_id == viajero.id, ViajeroActividad.actividad_id == id_actividad).first()
                if viajero_act_temp is None:
                    viajero_actividad = ViajeroActividad(viajero_id=viajero.id, actividad_id=id_actividad)
                    session.add(viajero_actividad)
            else:
                session.query(ViajeroActividad).filter(
                    ViajeroActividad.viajero_id == viajero.id, ViajeroActividad.actividad_id == id_actividad).delete()
        session.commit()
        return True

    def verGastosViajeroPorActividad(self, id_actividad):
        response = []
        viajeros_actividad = session.query(ViajeroActividad).filter(ViajeroActividad.actividad_id == id_actividad).all()
        if len(viajeros_actividad) < 1:
            return response
        for viajero_actividad in viajeros_actividad:
            viajero = session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).first()
            if viajero is not None:
                gastos = session.query(Gasto).filter(Gasto.viajero == viajero.id).all()
                totalPorViajero = 0
                if gastos is not None:
                    for gasto in gastos:
                        totalPorViajero += gasto.valor
                response.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido, "Valor": totalPorViajero})
        return response

    def darViajeroPorId(self, id_viajero):
        viajero = session.query(Viajero).filter(Viajero.id == id_viajero).first()
        return viajero

    def darViajeros(self):
        self.viajeros = session.query(Viajero).all()
        if len(self.viajeros) == 0:
            return []
        else:
            return self.viajeros

    def darViajerosAsociadosEnActividad(self, id_actividad):
        viajeros_actividad = session.query(ViajeroActividad).filter(ViajeroActividad.actividad_id == id_actividad).all()
        retorno = []
        for viajero_actividad in viajeros_actividad:
            retorno.extend(session.query(Viajero).filter(Viajero.id == viajero_actividad.viajero_id).all())
        return retorno

    def darViajerosPorActividad(self, id_actividad):
        viajeros = session.query(Viajero).all()
        if len(viajeros) < 1:
            return []
        viajeros_actividad = session.query(ViajeroActividad).filter(ViajeroActividad.actividad_id == id_actividad).all()
        if len(viajeros_actividad) > 0:
            for viajero in viajeros:
                viajero_presente = list(filter(lambda viajero_actividad: viajero_actividad.viajero_id == viajero.id,
                                               viajeros_actividad))
                viajero.presente = len(viajero_presente) > 0
        return viajeros
