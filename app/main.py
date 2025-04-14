from fastapi import FastAPI
from app.routers import tables, reservations

app = FastAPI(
    title="Сервис бронирования столиков",
    description="API для управления бронированиями столиков в ресторане",
    version="1.0.0",
)

app.include_router(tables.router, prefix="/tables", tags=["Tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])