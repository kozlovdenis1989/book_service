from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DeskCreate(BaseModel):
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., description="Количество мест за столиком")
    location: str = Field(..., description="Место расположения столика")

class DeskResponse(DeskCreate):
    id: int = Field(..., description="Идентификатор столика")

    model_config = ConfigDict(from_attributes=True) 

class ReservationCreate(BaseModel):
    customer_name: str = Field(..., description="Имя клиента")
    desk_id: int = Field(..., description="Идентификатор столика")
    reservation_time: datetime = Field(..., description="Время бронирования")
    duration_minutes: int = Field(..., description="Длительность брони в минутах")

class ReservationResponse(ReservationCreate):
    id: int = Field(..., description="Идентификатор брони")

    model_config = ConfigDict(from_attributes=True)