from typing import Optional
from sqlmodel import select
from models.apostador import Apostador
from database import SessionDep


class ApostadorRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_mail(self, mail: str) -> Optional[Apostador]:
        statement = select(Apostador).where(Apostador.mail == mail)
        return self.session.exec(statement).first()
    
    def save(self, apostador: Apostador):
        self.session.add(apostador)
        self.session.commit()
        self.session.refresh(apostador)
