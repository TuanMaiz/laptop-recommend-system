from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from api.db.session import Base  # from your SQLAlchemy setup


class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(String, primary_key=True, index=True)  # Assuming UUID or custom ID
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    specifications = Column(JSON, nullable=True)  # Stores Dict[str, Any]
    image_url = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=True, default=0)
    category = Column(String, nullable=True)
    processor = Column(String, nullable=True)
    ram = Column(String, nullable=True)
    storage = Column(String, nullable=True)
    graphics_card = Column(String, nullable=True)
    screen_size = Column(String, nullable=True)
    operating_system = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    battery_life = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
