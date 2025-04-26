from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.exceptions import DeskNotFound, DeskAlreadyExists

class DeskService:
    def __init__(self, db: Session):
        self.db = db

    def create_desk(self, desk: schemas.DeskCreate):
        db_desk = models.Desk(**desk.model_dump())
        self.db.add(db_desk)

        try:
            self.db.commit()
            self.db.refresh(db_desk)
            return db_desk
        except IntegrityError:
            self.db.rollback()
            raise DeskAlreadyExists()  

    def get_desks(self):
        return self.db.query(models.Desk).all()

    def delete_desk(self, desk_id: int):
        db_desk = self.db.query(models.Desk).filter(models.Desk.id == desk_id).first()
        if db_desk is None:
            raise DeskNotFound()  
        
        self.db.delete(db_desk)
        self.db.commit()
        return {"message": "Desk deleted"}