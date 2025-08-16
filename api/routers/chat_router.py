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
    apikey = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
        base_url="https://routellm.abacus.ai/v1",
        api_key=apikey,
    )

    stream = False  # or False
    chat_completion = client.chat.completions.create(
        model="route-llm",
        messages=[{"role": "user", "content": req.message}],
        stream=stream,
    )
    if stream:
        response_content = ""
        for event in chat_completion:
            if event.choices[0].finish_reason:
                break
            else:
                if event.choices[0].delta and event.choices[0].delta.content:
                    response_content += event.choices[0].delta.content
        return {"response": response_content}
    else:
        return {"response": chat_completion.choices[0].message.content}
