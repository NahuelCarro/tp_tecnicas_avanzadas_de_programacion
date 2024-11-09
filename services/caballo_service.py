from typing import Optional


from models.caballo import Caballo
from repository.caballo_repository import CaballoRepository
from exceptions import CaballoNoEncontradoException, CaballoDuplicadoException


class CaballoService:
    def __init__(self, caballo_repository: CaballoRepository):
        self.caballo_repository = caballo_repository

    def crear_caballo(self, nombre: str, peso: float):
        if self.caballo_repository.obtener_por_nombre(nombre):
            raise CaballoDuplicadoException()
        caballo = Caballo(nombre=nombre, peso=peso)
        self.caballo_repository.guardar(caballo)
        return caballo

    def obtener_caballo(self, nombre: str) -> Optional[Caballo]:
        caballo = self.caballo_repository.obtener_por_nombre(nombre)
        if not caballo:
            raise CaballoNoEncontradoException()
        return caballo
