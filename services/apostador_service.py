from typing import Optional
from fastapi import HTTPException
from models.apostador import Apostador
from models.apuesta import Apuesta
from repository.apostador_repository import ApostadorRepository
from repository.caballo_repository import CaballoRepository
from services.caballo_service import CaballoService
from repository.carrera_repository import CarreraRepository
from services.carrera_service import CarreraService
from repository.apuesta_repository import ApuestaRepository
from services.apuesta_service import ApuestaService


class ApostadorService:
    def __init__(
        self,
        apostador_repository: ApostadorRepository,
    ):
        self.apostador_repository = apostador_repository

    def crear_apostador(
        self, nombre: str, mail: str, clave: str, es_admin: bool
    ) -> Apostador:
        if self.apostador_repository.obtener_por_mail(mail):
            raise HTTPException(
                status_code=400,
                detail="Ya existe un apostador con ese mail",
            )

        apostador = Apostador(
            nombre=nombre, mail=mail, clave=clave, es_admin=es_admin
        )
        self.apostador_repository.guardar(apostador)
        return apostador

    def obtener_apostador(self, mail: str) -> Optional[Apostador]:
        return self.apostador_repository.obtener_por_mail(mail)

    def apostar(
        self,
        mail: str,
        carrera_id: int,
        nombre_caballo: str,
        monto: float
    ) -> Apuesta:
        apostador = self.apostador_repository.obtener_por_mail(mail)
        session = self.apostador_repository.session

        caballo_repository = CaballoRepository(session)
        caballo_service = CaballoService(caballo_repository)
        caballo = caballo_service.obtener_caballo(nombre_caballo)

        carrera_repository = CarreraRepository(session)
        carrera_service = CarreraService(carrera_repository)
        carrera = carrera_service.obtener_carrera_por_id(carrera_id)

        if monto < 0:
            raise HTTPException(
                status_code=400, detail="El monto no puede ser negativo"
            )
        if carrera.esta_iniciada():
            raise HTTPException(
                status_code=400, detail="La carrera ya ha iniciado"
            )
        if caballo not in carrera.caballos:
            raise HTTPException(
                status_code=400, detail="El caballo no está inscrito en la carrera"
            )
        if any(apuesta.apostador_id == apostador.id for apuesta in carrera.apuestas):
            raise HTTPException(
                status_code=400, detail="El apostador ya ha apostado en la carrera"
            )
        apuesta = apostador.apostar(caballo, carrera, monto)
        apuesta_repository = ApuestaRepository(session)
        apuesta_service = ApuestaService(apuesta_repository)
        apuesta_service.crear_apuesta(apuesta)
        carrera_service.actualizar_carrera(carrera)
        self.apostador_repository.guardar(apostador)
        return apuesta
