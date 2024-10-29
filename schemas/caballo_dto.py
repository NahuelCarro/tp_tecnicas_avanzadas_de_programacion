from sqlmodel import SQLModel

from models.caballo import Caballo


class CaballoDTO(SQLModel):
    def __init__(self, caballo: Caballo):
        self.nombre = caballo.nombre
        self.peso = caballo.peso
        self.cuota = caballo.cuota
