from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class User(UserBase):
    id: int
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    total_copies: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available_copies: int
    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    book_id: int

class TransactionCreate(TransactionBase):
    user_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int
    issue_date: datetime.date
    return_date: Optional[datetime.date] = None
    model_config = ConfigDict(from_attributes=True)
