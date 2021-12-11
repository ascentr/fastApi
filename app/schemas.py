from os import access
from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint




from sqlalchemy.sql.sqltypes import Boolean

from app.database import Base


#create a PostBase class and let other classes inherit from PostBase(BaseModel)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    msg = 'Successfully created user'
    msg : str
    id : int
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str



class PostBase(BaseModel):
    title  : str
    content : str
    published : bool = True


#PostCreate will inherit all the fields The 'owner_id is set to current user the posts.py experiment with setting in create class
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True


#specify or omit any fields not required in response
class PostResponse(PostBase):
    id : int
    created_at: datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post : Post
    votes: int

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)
    
