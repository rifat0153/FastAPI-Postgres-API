from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# User Schema
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    pass

    class Config:
        orm_mode = True
