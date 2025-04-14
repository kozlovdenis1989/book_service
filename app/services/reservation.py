from sqlalchemy.orm import Session
from app import models, schemas
from app.exceptions import TableNotFound, TimeSlotTaken, ReservationNotFound
from datetime import timedelta

class ReservationService:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, reservation: schemas.ReservationCreate):
        if reservation.duration_minutes < 1:
            reservation.duration_minutes = 1

        db_table = self.db.query(models.Table).filter(models.Table.id == reservation.table_id).first()
        if db_table is None:
            raise TableNotFound()  

        end_time = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)
        conflicting_reservations = self.db.query(models.Reservation).filter(
            models.Reservation.table_id == reservation.table_id,
            models.Reservation.reservation_time < end_time,
            (models.Reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)) > reservation.reservation_time
        ).all()

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