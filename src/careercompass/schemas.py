from datetime import datetime

from pydantic import BaseModel


# Completed Tasks
class CompletedTask(BaseModel):
    id: int
    description: str = None
    created_at: datetime = None


class CreateCompletedTask(BaseModel):
    description: str


# Users
class UserBase(BaseModel):
    email: str | None = None
    full_name: str | None = None


class CreateUser(UserBase):
    password: str


class User(UserBase):
    is_active: bool | None = None

    class Config:
        orm_mode = True
        from_attributes=True


class UserInDB(User):
    id: int
    hashed_password: str


# Authentication and Tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class ErrorResponse(BaseModel):
    detail: str
