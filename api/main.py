from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from api.routers import laptop_router

app = FastAPI(title="Laptop Recommendation API")

app.include_router(laptop_router.router)


@app.get("/")
def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
