from typing import Optional
from sqlalchemy.orm import Session
from models.apostador import Apostador


class ApostadorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_mail(self, mail: str) -> Optional[Apostador]:
        return self.db.query(Apostador).filter(Apostador.mail == mail).first()
    
    def save(self, apostador: Apostador):
        self.db.add(apostador)
        self.db.commit()
        self.db.refresh(apostador)
