from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# разрешаем запросы из Mini App

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# временное хранилище (в памяти)

storage = {}

class Item(BaseModel):
name: str
qty: float

class SaveRequest(BaseModel):
user_id: int
group: str
items: List[Item]

@app.get("/")
def root():
return {"status": "API работает"}

@app.post("/save")
def save_data(data: SaveRequest):
key = f"{data.user_id}_{data.group}"
storage[key] = data.items
return {"status": "saved", "items": len(data.items)}

@app.get("/data")
def get_data(user_id: int, group: str):
key = f"{user_id}_{group}"
return storage.get(key, [])
