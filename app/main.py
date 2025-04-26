from fastapi import FastAPI
from app.routers import desks, reservations

app = FastAPI(
    title="Сервис бронирования столиков",
    description="API для управления бронированиями столиков в ресторане",
    version="1.0.0",
)

app.include_router(desks.router, prefix="/desks", tags=["Desks"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])