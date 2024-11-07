from sqlmodel import SQLModel
from datetime import datetime
from pydantic import Field

from models.carrera import Carrera
from schemas.caballo_dto import CaballoDTO


class CarreraCreacionDTO(SQLModel):
    fecha: datetime = Field(description="La fecha de la carrera")


class CarreraDTO(CarreraCreacionDTO):
    def __init__(self, carrera: Carrera):
        self.fecha = carrera.fecha


class CarreraConCaballosDTO(CarreraDTO):
    caballos: list[CaballoDTO] = Field(description="Los caballos de la carrera")

    def __init__(self, carrera: Carrera):
        super().__init__(carrera)
        self.caballos = [CaballoDTO(caballo) for caballo in carrera.caballos]


class CarreraConCaballoGanadorDTO(CarreraDTO):
    caballo_ganador: CaballoDTO = Field(description="El caballo ganador de la carrera")

    def __init__(self, carrera: Carrera):
        super().__init__(carrera)
        self.caballo_ganador = CaballoDTO(carrera.caballo_ganador)
