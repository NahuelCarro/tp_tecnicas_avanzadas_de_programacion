from sqlmodel import SQLModel

from models.apuesta import Apuesta


class ApuestaDTO(SQLModel):
    def __init__(self, apuesta: Apuesta):
        self.monto = apuesta.monto
        self.fecha = apuesta.fecha
        self.carrera_id = apuesta.carrera.id
        self.caballo_id = apuesta.caballo.id
