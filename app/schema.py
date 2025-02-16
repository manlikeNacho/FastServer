from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

from sqlalchemy import UUID


class Item(BaseModel):
    title: str
    content: str = "This is the default content"
    rating: Optional[int] = None


class User(BaseModel):
    email: EmailStr
    name: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResp(BaseModel):
    id: str
    email: EmailStr

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserLogin(BaseModel):
    email: str
    password: str


class UserLoginResp(BaseModel):
    email: str
    address: Optional[str] = None  # Use Optional for nullable fields
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
