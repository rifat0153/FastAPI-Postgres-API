import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import time

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(
            host="localhost",
            database='fastapi',
            user='postgres', password='Lampard08', cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("DB connection successful")

        break

    except Exception as error:
        print("Connecting to DB failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    if(post.rating == 1):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id not found"}

    cursor.execute(
        """ INSERT INTO posts (title,content, published) VALUES (%s, %s, %s)  RETURNING * """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()

    conn.commit()

    return {
        "data": new_post
    }


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts 
        WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    return {"post": post}


@app.delete("/posts/{id}")
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s 
        RETURNING *
     """, (str(id),))

    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET 
        title = %s, 
        content = %s,
        published = %s
        WHERE id = %s
        RETURNING *
     """, (post.title, post.content, post.published, str(id,)
           )
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    return {"post": updated_post}
