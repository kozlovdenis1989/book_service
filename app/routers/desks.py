from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, schemas
from app.services.desk import DeskService
from app.exceptions import DeskNotFound, DeskAlreadyExists

router = APIRouter()

@router.post("/", response_model=schemas.DeskResponse, summary="Создание нового столика", description="Создает новый столик в ресторане.")
def create_desk(desk: schemas.DeskCreate, db: Session = Depends(db.get_db)):
    desk_service = DeskService(db)
    try:
        db_desk = desk_service.create_desk(desk)
        return db_desk
    except DeskAlreadyExists as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.get("/", response_model=list[schemas.DeskResponse], summary="Получение всех столиков", description="Возвращает список всех столиков в ресторане.")
def get_desks(db: Session = Depends(db.get_db)):
    desk_service = DeskService(db)
    return desk_service.get_desks()

@router.delete("/{desk_id}", summary="Удаление столика", description="Удаляет столик из системы по его идентификатору.")
def delete_desk(desk_id: int, db: Session = Depends(db.get_db)):
    desk_service = DeskService(db)
    try:
        result = desk_service.delete_desk(desk_id)
        return result
    except DeskNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)