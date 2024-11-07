from sqlmodel import SQLModel
from pydantic import Field
from models.caballo import Caballo


class CaballoDTO(SQLModel):
    nombre: str = Field(description="El nombre del caballo")
    peso: float = Field(description="El peso del caballo")

    def __init__(self, caballo: Caballo):
        self.nombre = caballo.nombre
        self.peso = caballo.peso
