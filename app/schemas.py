from pydantic import BaseModel, EmailStr
from typing import Optional

class ParentBase(BaseModel):
    email: EmailStr

class ParentCreate(ParentBase):
    first_name: str
    last_name: str
    age: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    password: str
    profile_photo: Optional[str] = None

class Parent(ParentBase):
    id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    age: Optional[int]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    pincode: Optional[str]
    is_active: bool
    profile_photo: Optional[str]

    class Config:
        orm_mode = True


class ParentUpdate(ParentBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    email: Optional[str] = None
    profile_photo: Optional[str] = None

class ChildBase(BaseModel):
    name: str

class ChildCreate(ChildBase):

    
    pass

class Child(ChildBase):
    child_id: int
    parent_id: int

    class Config:
        orm_mode = True

