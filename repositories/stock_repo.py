from turtle import st
from unicodedata import name
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from entities.models.stock import Stock
from entities.schemas.stock import Stock as stock_schema
from entities.schemas.stock import StockData as stock_data_schema
from sqlalchemy import desc


async def create(stock: Stock, db: Session):
    if not db.query(stock_schema).filter(stock_schema.id == stock.stock_id).first():
        new_stock = stock_schema(id=stock.stock_id,
                                 name=stock.name)
        db.add(new_stock)
        db.commit()
    new_stock_data = stock_data_schema(id=stock.stock_id,
                                       time_stamp=stock.timestamp,
                                       price=stock.price,
                                       availability=stock.availability)
    db.add(new_stock_data)
    db.commit()
    return {"Status":"Successful"}

async def get_stock(id:str, db: Session):
    stock = (db.query(stock_schema).filter(stock_schema.id == id).first()).__dict__
    stock_data = (db.query(stock_data_schema).filter(stock_data_schema.id == id).order_by(desc('time_stamp')).first()).__dict__
    stock.update(stock_data)
    stock["stock_id"] = stock.pop("id")
    stock["timestamp"] = stock.pop("time_stamp")
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Stock with the id {id} is not available")
    return stock