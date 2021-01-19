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

    class Config:
        schema_extra = {
            "example": {
                "firstname": "Mark",
                "lastname": "Zuckerberg",
                "email": "reptil@facebook.com",
                "phonenumber": "650-543-4800",
                "country": "USA",
                "birthdate": "1984-05-14",
                "photo": "https://melmagazine.com/wp-content/uploads/"
                + "2020/07/zuck_sunscreen.jpg",
            }
        }


class UserDB(UserSchema):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "firstname": "Mark",
                "lastname": "Zuckerberg",
                "email": "reptil@facebook.com",
                "phonenumber": "650-543-4800",
                "country": "USA",
                "birthdate": "1984-05-14",
                "photo": "https://melmagazine.com/wp-content/uploads/"
                + "2020/07/zuck_sunscreen.jpg",
                "id": 16,
            }
        }


class UserListSchema(BaseModel):
    amount: int
    users: List[UserDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 2,
                "users": [
                    {
                        "firstname": "Mark",
                        "lastname": "Zuckerberg",
                        "email": "reptil@facebook.com",
                        "phonenumber": "650-543-4800",
                        "country": "USA",
                        "birthdate": "1984-05-14",
                        "photo": "https://melmagazine.com/wp-content/"
                        + "uploads/2020/07/zuck_sunscreen.jpg",
                        "id": 14,
                    },
                    {
                        "firstname": "Jack",
                        "lastname": "Dorsey",
                        "email": "barba@twitter.com",
                        "phonenumber": "212-300-8876",
                        "country": "USA",
                        "birthdate": "1976-11-19",
                        "photo": "https://i.insider.com/5e5e32fafee23d6a26433d83?"
                        + "width=750&format=jpeg&auto=webp",
                        "id": 9,
                    },
                ],
            }
        }


class UserUpdateSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phonenumber: Optional[str] = None
    country: Optional[str] = None
    birthdate: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "firstname": "Marquitos",
                "lastname": "Zucaritas",
            }
        }


class WalletDB(BaseModel):
    uuid: int
    address: str
    mnemonic: str
    balance: float

    class Config:
        schema_extra = {
            "example": {
                "uuid": 1,
                "address": "ABCDEF123",
                "mnemonic": "word word word word word word word",
                "balance": 0.24
            }
        }
