from sqlalchemy import Column, Integer, String, Date, ForeignKey

from .declarative_base import Base


class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    concepto = Column(String)
    valor = Column(Integer)
    fecha = Column(Date)
    viajero = Column(Integer, ForeignKey('viajero.id'))
    actividad = Column(Integer, ForeignKey('actividad.id'))