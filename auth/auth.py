import os
from typing import Annotated
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from database import SessionDep
from models.apostador import Apostador
from services.apostador_service import ApostadorService
from repository.apostador_repository import ApostadorRepository
from auth.exceptions import (
    InvalidCredentialsException,
    ExpiredTokenException,
    UserNotFoundException,
)


# Configuracion del JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/apostador")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="apostador/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> Apostador:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        mail: str = payload.get("sub")
        if mail is None:
            raise InvalidCredentialsException()
    except ExpiredSignatureError:
        raise ExpiredTokenException()
    except JWTError:
        raise InvalidCredentialsException()

    apostador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(apostador_repository)
    apostador = apostador_service.obtener_apostador(mail)
    if apostador is None:
        raise UserNotFoundException()
    return apostador
