from fastapi import HTTPException
from models.apostador import Apostador
from repository.apostador_repository import ApostadorRepository


class ApostadorService:
    def __init__(
        self,
        apostador_repository: ApostadorRepository,
    ):
        self.apostador_repository = apostador_repository

    def crear_apostador(
        self, nombre: str, mail: str, clave: str, es_admin: bool
    ) -> Apostador:
        if self.apostador_repository.get_by_mail(mail):
            raise HTTPException(
                status_code=400, detail="Ya existe un apostador con ese mail"
            )

        apostador = Apostador(nombre=nombre, mail=mail, clave=clave, es_admin=es_admin)
        self.apostador_repository.save(apostador)
        return apostador
