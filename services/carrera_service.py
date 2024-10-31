from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status

from models.carrera import Carrera
from models.caballo import Caballo
from repository.carrera_repository import CarreraRepository


class CarreraService:
    def __init__(self, carrera_repository: CarreraRepository):
        self.carrera_repository: CarreraRepository = carrera_repository

    def obtener_carreras_disponibles(
        self,
        cantidad_por_pagina: int = 10,
        pagina: int = 0
    ):
        fecha_actual = datetime.now()
        return self.carrera_repository.obtener_carreras_disponibles(
            fecha_actual, cantidad_por_pagina, pagina
        )

    def crear_carrera(self, fecha: datetime):
        if fecha < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de la carrera no puede ser del pasado"
            )
        carrera = Carrera(fecha=fecha)
        self.carrera_repository.guardar(carrera)
        return carrera

    def agregar_caballo(self, carrera: Carrera, caballo: Caballo):
        carrera_obtenida: Carrera = self.carrera_repository.obtener_por_id(
            carrera.id
        )
        if not carrera_obtenida:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrera no encontrada"
            )
        if carrera_obtenida.esta_iniciada():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La carrera ya ha comenzado"
            )
        carrera_obtenida.inscribir_caballo(caballo)
        self.carrera_repository.guardar(carrera_obtenida)
        return carrera_obtenida

    def empezar_carrera(self, carrera: Carrera):
        if not carrera.esta_iniciada():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La carrera no ha comenzado"
            )
        if carrera.caballo_ganador_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La carrera ya ha terminado"
            )
        try:
            carrera.determinar_ganador()
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        self.carrera_repository.guardar(carrera)
        return carrera

    def obtener_carrera_por_id(self, id: int) -> Optional[Carrera]:
        carrera = self.carrera_repository.obtener_por_id(id)
        if not carrera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrera no encontrada"
            )
        return carrera
