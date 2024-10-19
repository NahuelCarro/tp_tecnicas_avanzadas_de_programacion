import bcrypt
from fastapi import APIRouter, status
from schemas.apostador_dto import ApostadorRegistroDTO, ApostadorDTO
from services.apostador_service import ApostadorService
from repository.apostador_repository import ApostadorRepository
from database import SessionDep

router = APIRouter(prefix="/apostador")


@router.post(
    "/registrar",
    response_model=ApostadorDTO,
    status_code=status.HTTP_201_CREATED
)
def registrar_apostador(
    apostador: ApostadorRegistroDTO, session: SessionDep
) -> ApostadorDTO:
    aporador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(aporador_repository)
    clave = bcrypt.hashpw(apostador.clave.encode("utf-8"), bcrypt.gensalt())
    return ApostadorDTO(
        apostador_service.crear_apostador(
            apostador.nombre, apostador.mail, clave, apostador.es_admin
        )
    )
