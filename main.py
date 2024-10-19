from fastapi import FastAPI
from controllers import apostador_controller

from database import create_db_and_tables

app = FastAPI()

create_db_and_tables()
app.include_router(apostador_controller.router)
