from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.exceptions import TableNotFound, TableAlreadyExists

class TableService:
    def __init__(self, db: Session):
        self.db = db

    def create_table(self, table: schemas.TableCreate):
        db_table = models.Table(**table.model_dump())
        self.db.add(db_table)

        try:
            self.db.commit()
            self.db.refresh(db_table)
            return db_table
        except IntegrityError:
            self.db.rollback()
            raise TableAlreadyExists()  

    def get_tables(self):
        return self.db.query(models.Table).all()

    def delete_table(self, table_id: int):
        db_table = self.db.query(models.Table).filter(models.Table.id == table_id).first()
        if db_table is None:
            raise TableNotFound()  
        
        self.db.delete(db_table)
        self.db.commit()
        return {"message": "Table deleted"}