from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

DATA_FILE = "storage.json"

class Item(BaseModel):
name: str
qty: float

class SaveRequest(BaseModel):
user_id: int
group: str
items: List[Item]

@app.get("/")
def root():
return {"status": "ok"}

@app.post("/save")
def save_data(data: SaveRequest):

```
storage = {}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        storage = json.load(f)

key = str(data.user_id) + "_" + data.group

storage[key] = []

for item in data.items:
    storage[key].append({
        "name": item.name,
        "qty": item.qty
    })

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(storage, f)

return {"status": "saved"}
```

@app.get("/data")
def get_data(user_id: int, group: str):

```
if not os.path.exists(DATA_FILE):
    return []

with open(DATA_FILE, "r", encoding="utf-8") as f:
    storage = json.load(f)

key = str(user_id) + "_" + group

if key not in storage:
    return []

return storage[key]
```
