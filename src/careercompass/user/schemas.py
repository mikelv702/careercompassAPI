from pydantic import BaseModel


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