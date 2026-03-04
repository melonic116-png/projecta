from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# разрешаем запросы из Mini App

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

DATA_FILE = "storage.json"
ITEMS_FILE = "items.json"

def load_json(path):
if not os.path.exists(path):
return {}
with open(path, "r", encoding="utf-8") as f:
return json.load(f)

def save_json(path, data):
with open(path, "w", encoding="utf-8") as f:
json.dump(data, f, ensure_ascii=False)

storage = load_json(DATA_FILE)
items = load_json(ITEMS_FILE)

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

@app.get("/items")
def get_items(group: str):
return items.get(group, [])

@app.post("/save")
def save_data(data: SaveRequest):
key = f"{data.user_id}_{data.group}"
storage[key] = [item.dict() for item in data.items]
save_json(DATA_FILE, storage)
return {"status": "saved", "items": len(data.items)}

@app.get("/data")
def get_data(user_id: int, group: str):
key = f"{user_id}_{group}"
return storage.get(key, [])
