from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from entities.models.stock import Stock
from config.hashing import get_password_hash
from entities.models.user import User,UpdateUser,CreditOperation,StockOperation
from entities.schemas.user import User as user_schema, UserStocks, PendingOperation
from routers.resources.strings import WITHDRAW,DEPOSIT,SELL,BUY
from .stock_repo import get_stock
from .stock_repo import create as create_stock

async def create(user: User, db: Session):
    new_user = user_schema( first_name=user.first_name,
                            last_name=user.last_name,
                            password=get_password_hash(user.password),
                            phone=user.phone,
                            email=user.email,
                            credit=user.credit)
    db.add(new_user)
    db.commit()
    return {"Status":"Successful"}

async def get_user(id:int, db: Session):
    user = db.query(user_schema).filter(user_schema.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

async def update_user(id: int, user: UpdateUser, db: Session):
    if(user['password']):
        user['password'] = get_password_hash(user['password'])

    user_query = db.query(user_schema).filter(user_schema.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")

    user_query.update({k: v for k, v in user.items() if v})
    db.commit()
    
    return {"Status":"Successful"}

async def operation(operation_data:CreditOperation,operation:str ,db: Session):
    user_query = db.query(user_schema).filter(user_schema.id == operation_data.user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {operation_data.user_id} is not available")
    if operation == DEPOSIT:
        user_query.update({"credit":user.credit+operation_data.amount})
    elif  operation == WITHDRAW:
        user_query.update({"credit":user.credit-operation_data.amount})
    else:
        {"Error":"Unvalid Operation"}
    db.commit()
    return {"Status":"Successful"}

async def buy_operation(operation_data:StockOperation,db:Session):
    user_query = db.query(user_schema).filter(user_schema.id == operation_data.user_id)
    user = user_query.first()
    stock = await get_stock(operation_data.stock_id,db)
    if(user.credit < stock["price"]*operation_data.total):
        return {"Error":"Not Enough Credit"}
    if(operation_data.total>stock["availability"]):
        return {"Error":"Not Enough Available Stocks"}
    if(operation_data.lower_bound>stock["price"] or operation_data.upper_bound<stock["price"]):
        new_pending_operation = PendingOperation(stock_id=operation_data.stock_id,
                                        user_id=operation_data.user_id,
                                        amount=operation_data.total,
                                        upper_bound=operation_data.upper_bound,
                                        lower_bound=operation_data.lower_bound,
                                        operation_type=BUY)
        db.add(new_pending_operation)
        db.commit()
        return {"Status":"Operation Pending"}
    user_query.update({"credit":user.credit-(stock["price"]*operation_data.total)})
    user_stock_query = db.query(UserStocks).filter(UserStocks.stock_id==operation_data.stock_id, UserStocks.user_id == operation_data.user_id)
    print("booo")
    user_stock = user_stock_query.first()
    if not user_stock:
        new_stock = UserStocks(stock_id=operation_data.stock_id,
                                user_id=operation_data.user_id,
                                amount=operation_data.total)
        stock["availability"] -= operation_data.total
        stock["timestamp"] = datetime.now()
        db.add(new_stock)
        await create_stock(Stock(**stock),db)
        db.commit()
        return {"Status":"Successful"}
    user_stock_query.update({"amount":user_stock.amount+operation_data.total})
    print("boho")
    stock["availability"] -= operation_data.total
    stock["timestamp"] = datetime.now()
    print(stock)
    await create_stock(Stock(**stock),db)
    db.commit()
    return {"Status":"Successful"}

async def sell_operation(operation_data:StockOperation,db:Session):
    user_query = db.query(user_schema).filter(user_schema.id == operation_data.user_id)
    user = user_query.first()
    stock = await get_stock(operation_data.stock_id,db)
    user_stock_query = db.query(UserStocks).filter(UserStocks.stock_id==operation_data.stock_id, UserStocks.user_id == operation_data.user_id)
    user_stock = user_stock_query.first()
    if not user_stock or  user_stock.amount < operation_data.total:
        return {"Error":"Not Enough Stocks"}
    if(operation_data.lower_bound>stock["price"] or operation_data.upper_bound<stock["price"]):
        new_pending_operation = PendingOperation(stock_id=operation_data.stock_id,
                                        user_id=operation_data.user_id,
                                        amount=operation_data.total,
                                        upper_bound=operation_data.upper_bound,
                                        lower_bound=operation_data.lower_bound,
                                        operation_type=SELL)
        db.add(new_pending_operation)
        db.commit()
        return {"Status":"Operation Pending"}
    user_stock_query.update({"amount":user_stock.amount-operation_data.total})
    user_query.update({"credit":user.credit+(stock["price"]*operation_data.total)})
    stock["availability"] += operation_data.total
    stock["timestamp"] = datetime.now()
    await create_stock(Stock(**stock),db)
    db.commit()
    return {"Status":"Successful"}

async def check_pending(stock: Stock, db: Session):
    operations = db.query(PendingOperation).filter(PendingOperation.lower_bound<=stock.price,PendingOperation.upper_bound>=stock.price,PendingOperation.stock_id==stock.stock_id)
    for operation in operations:
        operation_dict = operation.__dict__
        if operation.operation_type == SELL:
            res = await sell_operation(StockOperation(**operation_dict,total=operation_dict["amount"]),db)
        elif operation.operation_type == BUY:
            res = await buy_operation(StockOperation(**operation_dict,total=operation_dict["amount"]),db)
        else:
            return {"Error":"Operation Not Found"}
        if(res["Status"]):
            db.delete(operation)
            db.commit()
        return {"Status":"Successful"}