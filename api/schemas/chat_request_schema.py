from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str;
    fingerprint: str;
    ipAdress: str;
    
