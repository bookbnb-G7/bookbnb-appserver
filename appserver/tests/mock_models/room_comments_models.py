from tests.utils import MockResponse


class MockCommentResponse(MockResponse):
    def dict(self):
        return {
            "comment": "Nice room",
            "commentator": "Chayanne",
            "commentator_id": 27,
            "main_comment_id": None,
            "id": 3,
            "room_id": 7,
            "created_at": "2020-12-01T19:00:00.033Z",
            "updated_at": "2020-12-01T19:00:00.033Z",
        }


class MockCommentListResponse(MockResponse):
    def dict(self):
        return {
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
