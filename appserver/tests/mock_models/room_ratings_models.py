from tests.utils import MockResponse


class MockRatingResponse(MockResponse):
    def dict(self):
        return {
            "rating": 4,
            "reviewer": "string",
            "reviewer_id": 44,
            "id": 23,
            "room_id": 983,
            "created_at": "2020-11-10T22:51:03.539Z",
            "updated_at": "2020-11-10T22:51:03.539Z",
        }


class MockRatingListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 1,
            "ratings": [
                {
                    "rating": 5,
                    "reviewer": "carlito",
                    "reviewer_id": 0,
                    "id": 0,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "rating": 0,
                    "reviewer": "remalo",
                    "reviewer_id": 666,
                    "id": 2,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }
