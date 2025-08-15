import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import psycopg2
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop import Laptop

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    try:
        yield conn
    finally:
        conn.close()


@router.get("/laptops", response_model=List[Laptop])
def get_all_laptops(limit: int = 20, db: Session = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, name, brand, model, price, description, specifications, image_url, stock_quantity, category, processor, ram, storage, graphics_card, screen_size, operating_system, weight, battery_life
            FROM laptops
            ORDER BY id
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        laptops = [dict(zip(columns, row)) for row in rows]
    return laptops


@router.get("/laptop/{id}", response_model=dict)
def get_laptop_detail(id: int, db: Session = Depends(get_db)):
    with db.cursor() as cur:
        # Get laptop info
        cur.execute(
            """
            SELECT id, name, brand, model, price, description, specifications, image_url, stock_quantity, category, processor, ram, storage, graphics_card, screen_size, operating_system, weight, battery_life
            FROM laptops
            WHERE id = %s
            """,
            (id,),
        )
        laptop_row = cur.fetchone()
        if not laptop_row:
            raise HTTPException(status_code=404, detail="Laptop not found")
        columns = [desc[0] for desc in cur.description]
        laptop = dict(zip(columns, laptop_row))
    return laptop
