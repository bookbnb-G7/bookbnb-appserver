from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class RoomCommentSchema(BaseModel):
    comment: str
    main_comment_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "comment": "Nice room",
                "commentator": "Chayanne",
                "commentator_id": 27
            }
        }


class RoomCommentDB(RoomCommentSchema):
    id: int
    room_id: int
    commentator: str
    commentator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "comment": "Nice room",
                "commentator": "Chayanne",
                "commentator_id": 27,
                "main_comment_id": None,
                "id": 3,
                "room_id": 7,
                "created_at": "2020-12-01T19:00:00.033Z",
                "updated_at": "2020-12-01T19:00:00.033Z",
            }
        }


class RoomCommentWithAnswers(BaseModel):
    comment: RoomCommentDB
    answers: List[RoomCommentDB]

    class Config:
        schema_extra = {
            "example": {
                "comment": {
                    "comment": "Nice room",
                    "commentator": "Chayanne",
                    "commentator_id": 27,
                    "main_comment_id": None,
                    "id": 3,
                    "room_id": 7,
                    "created_at": "2020-12-01T19:00:00.033Z",
                    "updated_at": "2020-12-01T19:00:00.033Z",
                },
                "answers": []
            }
        }


class RoomCommentList(BaseModel):
    amount: int
    room_id: int
    comments: List[RoomCommentWithAnswers]

    class Config:
        schema_extra = {
            "example": {
                "amount": 1,
                "room_id": 7,
                "comments": [
                    {
                        "comment": {
                            "comment": "Nice room",
                            "commentator": "Chayanne",
                            "commentator_id": 27,
                            "main_comment_id": None,
                            "id": 3,
                            "room_id": 7,
                            "created_at": "2020-12-01T19:00:00.033Z",
                            "updated_at": "2020-12-01T19:00:00.033Z",
                        },
                        "answers": []
                    }
                ]
            }
        }
