from sqlalchemy import Column, String, Float, Integer, ForeignKey
from config.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'User'
    id  = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    credit = Column(Float)
    email =  Column(String)
    phone = Column(String)
    password = Column(String)
    stocks = relationship("Stock",secondary='UserStocks',cascade="all, delete",passive_deletes=True)
    operations = relationship("Stock",secondary='PendingOperation',cascade="all, delete",passive_deletes=True)

class UserStocks(Base):
    __tablename__ = 'UserStocks'
    stock_id = Column(String, ForeignKey('Stock.id'), primary_key = True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key = True)
    amount = Column(Integer)

class PendingOperation(Base):
    __tablename__ = 'PendingOperation'
    operation_type = Column(String)
    stock_id = Column(String, ForeignKey('Stock.id'), primary_key = True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key = True)
    amount = Column(Integer)
    upper_bound = Column(Float)
    lower_bound = Column(Float)