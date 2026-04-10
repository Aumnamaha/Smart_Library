from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import datetime

from database import engine, SessionLocal, Base
import models, schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Library API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes for Book Inventory
@app.get("/api/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@app.post("/api/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump(), available_copies=book.total_copies)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Routes for Users
@app.get("/api/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "hashed"
    db_user = models.User(username=user.username, password_hash=fake_hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Routes for Transactions (Issue/Return)
@app.post("/api/transactions/issue/", response_model=schemas.Transaction)
def issue_book(trans: schemas.TransactionCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == trans.book_id).first()
    if not book or book.available_copies < 1:
        raise HTTPException(status_code=400, detail="Book not available")
    
    book.available_copies -= 1
    db_trans = models.Transaction(user_id=trans.user_id, book_id=trans.book_id)
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans

@app.post("/api/transactions/return/{transaction_id}", response_model=schemas.Transaction)
def return_book(transaction_id: int, db: Session = Depends(get_db)):
    trans = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if trans.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    trans.return_date = datetime.datetime.utcnow()
    book = db.query(models.Book).filter(models.Book.id == trans.book_id).first()
    book.available_copies += 1
    
    db.commit()
    db.refresh(trans)
    return trans

@app.get("/api/transactions/", response_model=List[schemas.Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

# Serve Frontend
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")
