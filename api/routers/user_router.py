import os
from openai import OpenAI
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop_schema import LaptopBase
from api.schemas.chat_request_schema import ChatRequest
from api.db.models.laptop_model import Laptop
from api.services.user_profile_service import UserProfileNeo4j

# from api.services.chat_query_service import makeChat
router = APIRouter(prefix="/user")


class UserCreateRequest(BaseModel):
    fingerprint: str
    func_req: str
    prefers_range: str


@router.post("/create", summary="Create a new user")
def create_user(user: UserCreateRequest):
    """
    Create a new user and initialize ontology preferences.
    """
    try:
        user_service = UserProfileNeo4j()
        user_service.init_owl_local()
        user_service.create_or_update_user_preference(
            fingerprint=user.fingerprint,
            func_req=user.func_req,
            prefers_range=user.prefers_range,
        )
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
