from repository.caballo_repository import CaballoRepository
from models.caballo import Caballo
from fastapi import HTTPException
from typing import Optional


class CaballoService:
    def __init__(self, caballo_repository: CaballoRepository):
        self.caballo_repository = caballo_repository

    def crear_caballo(self, nombre: str, peso: float, cuota: float):
        if self.caballo_repository.obtener_por_nombre(nombre):
            raise HTTPException(
                status_code=400, detail="Ya existe un caballo con ese nombre"
            )
        caballo = Caballo(nombre=nombre, peso=peso, cuota=cuota)
        self.caballo_repository.guardar(caballo)
        return caballo

    def obtener_caballo(self, nombre: str) -> Optional[Caballo]:
        caballo = self.caballo_repository.obtener_por_nombre(nombre)
        if not caballo:
            raise HTTPException(status_code=404, detail="Caballo no encontrado")
        return caballo
