from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    desk_id = Column(Integer, ForeignKey('desks.id'))  # ссылка на desks.id
    reservation_time = Column(DateTime, default=datetime.utcnow)
    duration_minutes = Column(Integer)
    
    desk = relationship("Desk", back_populates="reservations")  

class Desk(Base):
    __tablename__ = 'desks'  # имя таблицы изменено
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    seats = Column(Integer)
    location = Column(String, unique=True)

    reservations = relationship("Reservation", cascade="all, delete-orphan", back_populates="desk") 