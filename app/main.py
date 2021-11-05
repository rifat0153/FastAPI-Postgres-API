from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"Hello": "World asd"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    if(post.rating == 1):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id not found"}

    return {
        "data": post.dict()
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
