from fastapi import FastAPI
from db import Base, SessionLocal, engine

app = FastAPI()


items = [{"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"}]

@app.get("/")
async def read_root() -> dict[str,str]:
    return {"Hello": "World Hello namste duniya"}

@app.get("/items/{item_id}")
def read_item(item_id:int) -> dict[str,str]:
    return items[item_id]