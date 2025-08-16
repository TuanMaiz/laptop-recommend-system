from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()  # loads .env file into environment
# Models for request/response
app = FastAPI(title="Laptop Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class LaptopBase(BaseModel):
    id: str
    title: str
    price: float
    
class LaptopDetail(LaptopBase):
    components: dict
    weight_kg: Optional[float] = None
    url: Optional[str] = None
    
from pydantic import BaseModel
    
class ChatRequest(BaseModel):
        message: str
@app.post("/chatbot")
async def chatbot(req: ChatRequest):
    from openai import OpenAI
    apikey = os.getenv("OPENAI_API_KEY")
    
    
    client = OpenAI(
        base_url="https://routellm.abacus.ai/v1",
        api_key=apikey,
    )
    
    stream = False # or False
    chat_completion = client.chat.completions.create(
    model="route-llm",
    messages=[
        {
        "role": "user",
        "content": req.message
        }
    ],
    stream=stream
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)