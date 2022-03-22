from pydantic import BaseModel
from typing import Optional, List

class BlogBase(BaseModel):
    title : str
    body  : str
    is_published : bool

    class Config():
        orm_mode = True

class Blog(BlogBase):
    id : int


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    id  : int
    name:str
    email:str
    blogs : List[Blog] =[]
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    id    : int
    title : str
    body  : str
    is_published : bool
    creator = ShowUser

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None