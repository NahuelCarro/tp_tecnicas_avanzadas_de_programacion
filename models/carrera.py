import random
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from models.carrera_caballo_link import CarreraCaballoLink


class Carrera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    fecha: datetime = Field(nullable=False)

    apuestas: list["Apuesta"] = Relationship(back_populates="carrera")
    caballos: list["Caballo"] = Relationship(
        back_populates="carreras", link_model=CarreraCaballoLink
    )
    caballo_ganador_id: Optional[int] = Field(default=None, foreign_key="caballo.id")
    caballo_ganador: Optional["Caballo"] = Relationship()

    def inscribir_caballo(self, caballo: "Caballo"):
        if caballo not in self.caballos:
            self.caballos.append(caballo)

    def esta_iniciada(self) -> bool:
        return self.fecha < datetime.now()

    def determinar_ganador(self):
        if not self.caballos:
            raise ValueError("No hay caballos para la carrera")
        ganador = random.choice(self.caballos)
        self.caballo_ganador = ganador
        self.caballo_ganador_id = ganador.id
