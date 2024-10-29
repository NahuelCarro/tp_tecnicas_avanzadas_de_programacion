import bcrypt
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, Depends, HTTPException

from database import SessionDep
from models.apostador import Apostador
from services.apostador_service import ApostadorService
from auth.auth import create_access_token, get_current_user
from repository.apostador_repository import ApostadorRepository
from schemas.apostador_dto import ApostadorRegistroDTO, ApostadorDTO

router = APIRouter(prefix="/apostador")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
    "/registrar",
    response_model=ApostadorDTO,
    status_code=status.HTTP_201_CREATED
)
def registrar_apostador(
    session: SessionDep, apostador: ApostadorRegistroDTO
) -> ApostadorDTO:
    aporador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(aporador_repository)
    clave = bcrypt.hashpw(apostador.clave.encode("utf-8"), bcrypt.gensalt())
    return ApostadorDTO(
        apostador_service.crear_apostador(
            apostador.nombre, apostador.mail, clave, apostador.es_admin
        )
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    apostador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(apostador_repository)
    apostador = apostador_service.obtener_apostador(form_data.username)
    is_psw_valid = bcrypt.checkpw(
        form_data.password.encode("utf-8"),
        apostador.clave
    )
    if not apostador or not is_psw_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": apostador.mail}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/perfil",
    response_model=ApostadorDTO,
    status_code=status.HTTP_200_OK
)
def perfil_apostador(
    current_user: Apostador = Depends(get_current_user)
) -> ApostadorDTO:
    return ApostadorDTO(current_user)
