from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from entities.models.stock import Stock
from routers.errors.generate_http_response_openapi import generate_response_for_openapi
from config.database import get_db
from repositories import stock_repo,user_repo

router = APIRouter(responses=generate_response_for_openapi("Stock"))

@router.get(
    "/{id}",
    response_model=Stock,
    status_code=status.HTTP_200_OK,
    summary="Get a stock",
    tags=["Stock"]
)
async def get(id:str, db: Session = Depends(get_db)):
    return await stock_repo.get_stock(id, db)

@router.post('/',
    status_code=status.HTTP_200_OK,
    summary="Add a stock",
    tags=["Stock"]
)
async def create(stock: Stock, db: Session = Depends(get_db)):
    res = await stock_repo.create(stock, db)
    await user_repo.check_pending(stock, db)
    return res