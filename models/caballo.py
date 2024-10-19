from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from models.carrera import Carrera
from models.carrera_caballo_link import CarreraCaballoLink


class Caballo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nombre: str = Field(nullable=False)
    peso: float = Field()
    cuota: float = Field(nullable=False)

    apuestas: list["Apuesta"] = Relationship(back_populates="caballo")
    carreras: list["Carrera"] = Relationship(
        back_populates="caballos", link_model=CarreraCaballoLink
    )

    def inscribir(self, carrera: Carrera):
        carrera.caballos.append(self)
