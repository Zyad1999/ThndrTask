from typing import List, Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

class Stock(BaseModel):
    stock_id:str
    name:str
    timestamp:datetime
    price:float
    availability:int