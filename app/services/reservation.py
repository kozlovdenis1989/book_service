from sqlalchemy.orm import Session
from app import models, schemas
from app.exceptions import DeskNotFound, TimeSlotTaken, ReservationNotFound
from datetime import timedelta
from sqlalchemy import text

class ReservationService:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, reservation: schemas.ReservationCreate):
        if reservation.duration_minutes < 1:
            reservation.duration_minutes = 1

        db_desk = self.db.query(models.Desk).filter(models.Desk.id == reservation.desk_id).first()
        if db_desk is None:
            raise DeskNotFound()  

        end_time = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)

        conflicting_reservations = self.db.query(models.Reservation).filter(
            models.Reservation.desk_id == reservation.desk_id,
            models.Reservation.reservation_time < end_time,
            text(
                "reservations.reservation_time + (reservations.duration_minutes || ' minutes')::interval > :reservation_time"
            )
        ).params(reservation_time=reservation.reservation_time).all()

        if conflicting_reservations:
            raise TimeSlotTaken()

        db_reservation = models.Reservation(**reservation.model_dump())
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation

    def get_reservations(self):
        return self.db.query(models.Reservation).all()

    def delete_reservation(self, reservation_id: int):
        db_reservation = self.db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise ReservationNotFound()

        self.db.delete(db_reservation)
        self.db.commit()
        return {"message": "Reservation deleted"}