import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import psycopg2
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop_schema import LaptopBase
from api.db.models.laptop_model import Laptop

router = APIRouter(prefix="/laptops")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[LaptopBase])
def list_laptops(limit: int = 20, db: Session = Depends(get_db)):
    laptops = db.query(Laptop).limit(limit).all()
    if not laptops:
        raise HTTPException(status_code=404, detail="No laptops found")
    return laptops


@router.get("/{id}", response_model=LaptopBase)
def get_laptop_detail(id: int, db: Session = Depends(get_db)):
    if not isinstance(id, str):
        id = str(id)
    laptop = db.query(Laptop).filter(Laptop.id == id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop
