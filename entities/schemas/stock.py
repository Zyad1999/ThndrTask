from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from config.database import Base
from sqlalchemy.orm import relationship

class Stock(Base):
    __tablename__ = 'Stock'
    id  = Column(String, primary_key=True)
    name = Column(String)
    data = relationship("StockData", back_populates="stock")

class StockData(Base):
    __tablename__ = 'StockData'
    id  = Column(String, ForeignKey(Stock.id, ondelete="CASCADE"), primary_key=True)
    time_stamp =  Column(DateTime, primary_key=True)
    price = Column(Float)
    availability = Column(Integer)
    stock = relationship(Stock, back_populates="data")