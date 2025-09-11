from sqlalchemy import Column, String, Numeric, Text, Integer, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from api.db.session import Base


class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    specifications = Column(JSON, nullable=True)
    image_url = Column(String(500), nullable=True)
    stock_quantity = Column(Integer, server_default="0")
    category = Column(Text, nullable=True)
    processor = Column(Text, nullable=True)
    ram = Column(Text, nullable=True)
    storage = Column(Text, nullable=True)
    graphics_card = Column(Text, nullable=True)
    screen_size = Column(Text, nullable=True)
    operating_system = Column(Text, nullable=True)
    weight = Column(Numeric(4, 2), nullable=True)
    battery_life = Column(Text, nullable=True)
    is_active = Column(Boolean, server_default="true")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
