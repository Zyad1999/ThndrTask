from typing import List, Optional
from pydantic import BaseModel,EmailStr
from entities.models.stock import Stock

class User(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    credit:float
    phone:str


class ShowUser(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    credit:float
    phone:str
    class Config():
        orm_mode = True
    
    
class UpdateUser(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[EmailStr]
    password:Optional[str]
    credit:Optional[float]
    phone:Optional[str]

class CreditOperation(BaseModel):
    user_id:int
    amount:int

class StockOperation(BaseModel):
    user_id:int
    stock_id:str
    total:int
    upper_bound:float
    lower_bound:float