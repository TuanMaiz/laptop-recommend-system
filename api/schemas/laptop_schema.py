# api/schemas/laptop_schema.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class LaptopBase(BaseModel):
    id: str
    name: str
    brand: str
    model: Optional[str]
    price: float
    description: Optional[str]
    specifications: Optional[Dict[str, Any]]
    image_url: Optional[str]
    stock_quantity: Optional[int]
    category: Optional[str]
    processor: Optional[str]
    ram: Optional[str]
    storage: Optional[str]
    graphics_card: Optional[str]
    screen_size: Optional[str]
    operating_system: Optional[str]
    weight: Optional[float]
    battery_life: Optional[str]
    is_active: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = (
            True  # 👈 very important so Pydantic can read from SQLAlchemy objects
        )
