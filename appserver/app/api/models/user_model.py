from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    phonenumber: str
    country: str
    birthdate: str
    photo: Optional[str] = None


class UserListSchema(BaseModel):
    amount: int
    users: List[UserSchema]


class UserUpdateSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phonenumber: Optional[str] = None
    country: Optional[str] = None
    birthdate: Optional[str] = None
