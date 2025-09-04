import os
from openai import OpenAI
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import psycopg2
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop_schema import LaptopBase
from api.schemas.chat_request_schema import ChatRequest
from api.db.models.laptop_model import Laptop
# from api.services.chat_query_service import makeChat
router = APIRouter(prefix="/chatbot")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def chatbot(req: ChatRequest):
    pass
    
