from typing import List, Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    reporter_id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    name: str
    address: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    uuid: str
    name: str
    is_active: bool
    vulns: List[Item] = []

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    is_active: bool