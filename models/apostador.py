from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from models.apuesta import Apuesta
from models.carrera import Carrera
from models.caballo import Caballo


class Apostador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    mail: str = Field(nullable=False, unique=True)
    clave: bytes = Field(nullable=False)
    balance_apuestas: float = Field(default=0.0)
    es_admin: bool = Field(default=False)

    apuestas: list[Apuesta] = Relationship(back_populates="apostador")

    def apostar(
        self,
        caballo: Caballo,
        carrera: Carrera,
        monto: float
    ) -> Apuesta:
        apuesta = Apuesta(
            monto=monto,
            apostador=self,
            caballo=caballo,
            carrera=carrera
        )
        self.apuestas.append(apuesta)
        carrera.apuestas.append(apuesta)
        return apuesta