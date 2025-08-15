# models.py - SQLAlchemy models
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import re
from datetime import datetime

Base = declarative_base()

class Laptop(Base):
    __tablename__ = 'laptops'
    
    id = Column(Integer, primary_key=True)
    neo4j_id = Column(String(255), unique=True)  # Matches Neo4j ID
    url = Column(String(255), unique=True)
    title = Column(String(255), nullable=False)
    price = Column(Float)
    price_display = Column(String(50))
    brand = Column(String(100))
    description = Column(Text)
    weight_kg = Column(Float)
    
    # Physical attributes
    material = Column(String(100))
    dimensions = Column(String(100))
    
    # System info
    os = Column(String(100))
    
    # Additional info
    warranty = Column(String(100))
    condition = Column(String(100))
    
    # Timestamps
    scraped_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    images = relationship("LaptopImage", back_populates="laptop")
    specifications = relationship("LaptopSpecification", back_populates="laptop")

class LaptopImage(Base):
    __tablename__ = 'laptop_images'
    
    id = Column(Integer, primary_key=True)
    laptop_id = Column(Integer, ForeignKey('laptops.id'))
    image_url = Column(String(255))
    is_primary = Column(Boolean, default=False)
    
    laptop = relationship("Laptop", back_populates="images")

class LaptopSpecification(Base):
    __tablename__ = 'laptop_specifications'
    
    id = Column(Integer, primary_key=True)
    laptop_id = Column(Integer, ForeignKey('laptops.id'))
    category = Column(String(50))  # CPU, RAM, Storage, etc.
    key = Column(String(100))      # Specific attribute name
    value = Column(Text)           # Value of the attribute
    
    laptop = relationship("Laptop", back_populates="specifications")
    
    __table_args__ = (
        UniqueConstraint('laptop_id', 'category', 'key', name='uix_spec'),
    )