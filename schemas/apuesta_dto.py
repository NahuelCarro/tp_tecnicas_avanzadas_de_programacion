from sqlmodel import SQLModel
from pydantic import Field
from datetime import datetime
from models.apuesta import Apuesta


class ApuestaDTO(SQLModel):
    monto: float = Field(description="El monto de la apuesta")
    fecha: datetime = Field(description="La fecha de la apuesta")
    carrera_id: int = Field(description="El ID de la carrera")
    caballo_nombre: str = Field(description="El nombre del caballo")

    def __init__(self, apuesta: Apuesta):
        self.monto = apuesta.monto
        self.fecha = apuesta.fecha
        self.carrera_id = apuesta.carrera.id
        self.caballo_nombre = apuesta.caballo.nombre
