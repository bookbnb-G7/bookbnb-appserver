from pydantic import BaseModel


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    phonenumber: str
    country: str
    birthdate: str


class UserDB(UserSchema):
    id: int
    updatedAt: str
    createdAt: str
