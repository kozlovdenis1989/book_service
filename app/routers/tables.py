from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, schemas
from app.services.table import TableService
from app.exceptions import TableNotFound, TableAlreadyExists

router = APIRouter()

@router.post("/", response_model=schemas.TableResponse, summary="Создание нового столика", description="Создает новый столик в ресторане.")
def create_table(table: schemas.TableCreate, db: Session = Depends(db.get_db)):
    table_service = TableService(db)
    try:
        db_table = table_service.create_table(table)
        return db_table
    except TableAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.get("/", response_model=list[schemas.TableResponse], summary="Получение всех столиков", description="Возвращает список всех столиков в ресторане.")
def get_tables(db: Session = Depends(db.get_db)):
    table_service = TableService(db)
    return table_service.get_tables()

@router.delete("/{table_id}", summary="Удаление столика", description="Удаляет столик из системы по его идентификатору.")
def delete_table(table_id: int, db: Session = Depends(db.get_db)):
    table_service = TableService(db)
    try:
        result = table_service.delete_table(table_id)
        return result
    except TableNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)