from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    table_id = Column(Integer, ForeignKey('tables.id'))
    reservation_time = Column(DateTime, default=datetime.utcnow)
    duration_minutes = Column(Integer)
    
    table = relationship("Table", back_populates="reservations")  


class Table(Base):
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    seats = Column(Integer)
    location = Column(String, unique=True)

    reservations = relationship("Reservation", cascade="all, delete-orphan", back_populates="table")  