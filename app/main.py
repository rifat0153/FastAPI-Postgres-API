from operator import pos
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import time
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.coercions import ReturnsRowsImpl
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# while True:

#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database='fastapi',
#             user='postgres', password='Lampard08', cursor_factory=RealDictCursor
#         )

#         cursor = conn.cursor()
#         print("DB connection successful")

#         break

#     except Exception as error:
#         print("Connecting to DB failed")
#         print("Error: ", error)
#         time.sleep(2)


@app.get("/test")
def testPost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.get("/posts")
def root(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ INSERT INTO posts (title,content, published) VALUES (%s, %s, %s)  RETURNING * """,
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()

    # conn.commit()
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post
    }


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts
    #     WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    return {"post": post}


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s
    #     RETURNING *
    #  """, (str(id),))

    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET
    #     title = %s,
    #     content = %s,
    #     published = %s
    #     WHERE id = %s
    #     RETURNING *
    #  """, (post.title, post.content, post.published, str(id,)
    #        )
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    old_post = post_query.first()

    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    post_query.update(
        post.dict(),
        synchronize_session=False)
    db.commit()

    return {"post": post_query.first()}
