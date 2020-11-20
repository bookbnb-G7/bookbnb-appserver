from typing import List, Optional
from pydantic import BaseModel


class UserReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: int

    class Config:
        schema_extra = {
            "example": {
                "review": "Excelente, prepara un buen guiso de lentejas",
                "reviewer": "Bob",
                "reviewer_id": 7,
            }
        }


class UserReviewUpdate(BaseModel):
    review: Optional[str] = None
    reviewer: Optional[str] = None
    reviewer_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "review": "Me cayo mal el guiso de lentejas",
            }
        }


UserReviewList = List[UserReviewSchema]
