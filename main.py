from fastapi import FastAPI
from routers import apostador_controller
from fastapi import HTTPException

from database import create_db_and_tables, get_session
from services.caballo_service import CaballoService
from repository.caballo_repository import CaballoRepository

app = FastAPI()

create_db_and_tables()
app.include_router(apostador_controller.router)

@app.on_event("startup")
def crear_caballos_iniciales():
    session = next(get_session())
    try:
        caballo_repo = CaballoRepository(session)
        caballo_service = CaballoService(caballo_repo)
        
        caballos_iniciales = [
            ("Relámpago", 450.5, 2.5),
            ("Tormenta", 480.0, 3.0),
            ("Fuego", 490.0, 2.7),
            ("Trueno", 500.0, 2.3),
            ("Ráfaga", 510.0, 2.1),
            ("Viento", 520.0, 1.9),
        ]
        
        for nombre, peso, cuota in caballos_iniciales:
            try:
                print(f"Creando caballo {nombre}...")
                caballo_service.crear_caballo(nombre, peso, cuota)
                print(f"Caballo {nombre} creado exitosamente.")
            except HTTPException:
                print(f"El caballo {nombre} ya existe. Saltando...")
                session.rollback()
        
        session.commit()
    except Exception as e:
        print(f"Error al crear caballos iniciales: {e}")
        session.rollback()
    finally:
        session.close()
