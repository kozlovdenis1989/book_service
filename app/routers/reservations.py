from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, schemas
from app.services.reservation import ReservationService
from app.exceptions import DeskNotFound, TimeSlotTaken, ReservationNotFound

router = APIRouter()

@router.post("/", response_model=schemas.ReservationResponse, summary="Создание новой брони", description="Создает новую бронь для указанного столика.")
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(db.get_db)):
    reservation_service = ReservationService(db)
    try:
        created_reservation = reservation_service.create_reservation(reservation)
        return created_reservation
    except (DeskNotFound, TimeSlotTaken) as e:
        raise HTTPException(status_code=404 if isinstance(e, DeskNotFound) else 400, detail=e.message)

@router.get("/", response_model=list[schemas.ReservationResponse], summary="Получение всех броней", description="Возвращает список всех броней в системе.")
def get_reservations(db: Session = Depends(db.get_db)):
    reservation_service = ReservationService(db)
    return reservation_service.get_reservations()

@router.delete("/{reservation_id}", summary="Удаление брони", description="Удаляет бронь из системы по её идентификатору.")
def delete_reservation(reservation_id: int, db: Session = Depends(db.get_db)):
    reservation_service = ReservationService(db)
    try:
        result = reservation_service.delete_reservation(reservation_id)
        return result
    except ReservationNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)