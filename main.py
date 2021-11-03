from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World asd"}


@app.post("/post")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"result": "successful"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
