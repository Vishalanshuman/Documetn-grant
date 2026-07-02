
from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True
