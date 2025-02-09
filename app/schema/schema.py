from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_time : datetime
    class Config:
        orm_mode = True
