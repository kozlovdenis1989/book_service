from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TableCreate(BaseModel):
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., description="Количество мест за столиком")
    location: str = Field(..., description="Место расположения столика")

class TableResponse(TableCreate):
    id: int = Field(..., description="Идентификатор столика")

    class Config(ConfigDict):
        from_attributes = True  

class ReservationCreate(BaseModel):
    customer_name: str = Field(..., description="Имя клиента")
    table_id: int = Field(..., description="Идентификатор столика")
    reservation_time: datetime = Field(..., description="Время бронирования")
    duration_minutes: int = Field(..., description="Длительность брони в минутах")

class ReservationResponse(ReservationCreate):
    id: int = Field(..., description="Идентификатор брони")

    class Config(ConfigDict):
        from_attributes = True 