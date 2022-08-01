from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from entities.models.user import (
    User,
    ShowUser,
    CreditOperation,
    StockOperation
)
from routers.errors.generate_http_response_openapi import generate_response_for_openapi
from routers.resources.strings import WITHDRAW,DEPOSIT
from config.database import get_db
from repositories import user_repo

router = APIRouter(responses=generate_response_for_openapi("User"))

@router.get(
    "/{int}",
    response_model=ShowUser,
    status_code=status.HTTP_200_OK,
    summary="Get a user",
    tags=["User"]
)
async def get(id:int, db: Session = Depends(get_db)):
    return await user_repo.get_user(id, db)

@router.post('/',
    status_code=status.HTTP_200_OK,
    summary="Add a user",
    tags=["User"]
)
async def create(user: User, db: Session = Depends(get_db)):
    return await user_repo.create(user, db)

@router.put('/deposit',
    status_code=status.HTTP_200_OK,
    summary="User deposit",
    tags=["User"]
)
async def deposit(deposit: CreditOperation, db: Session = Depends(get_db)):
    print(deposit.user_id)
    print(deposit.amount)
    return await user_repo.operation(deposit,DEPOSIT,db)

@router.put('/withdraw',
    status_code=status.HTTP_200_OK,
    summary="User withdraw",
    tags=["User"]
)
async def withdraw(withdraw: CreditOperation, db: Session = Depends(get_db)):
    return await user_repo.operation(withdraw,WITHDRAW,db)

@router.put('/buy',
    status_code=status.HTTP_200_OK,
    summary="User buy a stock",
    tags=["User"]
)
async def buy(buy: StockOperation, db: Session = Depends(get_db)):
    return await user_repo.buy_operation(buy,db)

@router.put('/sell',
    status_code=status.HTTP_200_OK,
    summary="User sell a stock",
    tags=["User"]
)
async def buy(sell: StockOperation, db: Session = Depends(get_db)):
    return await user_repo.sell_operation(sell,db)