from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Viajero(Base):
    __tablename__ = 'viajero'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    actividades = relationship('Actividad', secondary='viajero_actividad')
    presente = False