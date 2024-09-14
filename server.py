from typing import Union
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    query: str


@app.get("/api/ping")
async def read_ping():
    return {"status": 200, "message": "Ping!"}

@app.post("/api/query/text")
async def run_text(req: Item):
    print("got the request", req.query)
    result = model.predict(req.query)
    return {"status": 200, "message": result}
