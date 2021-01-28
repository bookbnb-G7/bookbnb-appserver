from tests.utils import MockResponse


class MockUserRatingResponse(MockResponse):
    def dict(self):
        return {
            "id": 3,
            "rating": 5,
            "reviewer": "aaaa",
            "reviewer_id": 2,
        }


class MockUserRatingListResponse(MockResponse):
    def dict(self):
        return {
            "userId": 8,
            "amount": 3,
            "ratings": [
                {
                    "id": 3,
                    "rating": 5,
                    "reviewer": "aaaa",
                    "reviewer_id": 2,
                },
                {
                    "id": 4,
                    "rating": 3,
                    "reviewer": "jon",
                    "reviewer_id": 4,
                },
                {
                    "id": 5,
                    "rating": 1,
                    "reviewer": "malaonda",
                    "reviewer_id": 5,
                },
            ],
        }
