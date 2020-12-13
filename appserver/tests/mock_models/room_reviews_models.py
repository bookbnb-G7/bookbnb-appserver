from tests.utils import MockResponse


class MockReviewResponse(MockResponse):
    def dict(self):
        return {
            "review": "muy lindo todo",
            "reviewer": "string",
            "reviewer_id": 44,
            "id": 23,
            "room_id": 22,
            "created_at": "2020-11-10T22:51:03.539Z",
            "updated_at": "2020-11-10T22:51:03.539Z",
        }


class MockReviewListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 1,
            "reviews": [
                {
                    "review": "muy lindo todo",
                    "reviewer": "carlitos",
                    "reviewer_id": 10,
                    "id": 0,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "review": "todo mal",
                    "reviewer": "remalo",
                    "reviewer_id": 666,
                    "id": 2,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }
