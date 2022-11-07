from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.modelo.Viajero import Viajero
from src.modelo.Gasto import Gasto

from .declarative_base import Base


class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    estaTerminada = Column(Boolean)
    viajeros = relationship('Viajero', secondary='viajero_actividad')
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')


class ViajeroActividad(Base):
    __tablename__ = 'viajero_actividad'

    viajero_id = Column(
        Integer,
        ForeignKey('viajero.id'),
        primary_key=True)

    actividad_id = Column(
        Integer,
        ForeignKey('actividad.id'),
        primary_key=True)