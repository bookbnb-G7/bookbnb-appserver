from tests.utils import MockResponse


class MockUserReviewResponse(MockResponse):
    def dict(self):
        return {
            "id": 3,
            "review": "sisi muy lindo todo la verdad",
            "reviewer": "aaaa",
            "reviewer_id": 2,
        }


class MockUserReviewListResponse(MockResponse):
    def dict(self):
        return {
            "userId": 8,
            "amount": 3,
            "reviews": [
                {
                    "id": 3,
                    "review": "sisi muy lindo todo la verdad",
                    "reviewer": "aaaa",
                    "reviewer_id": 6,
                },
                {
                    "id": 4,
                    "review": "sese muy lindo todo la verda",
                    "reviewer": "aaaa",
                    "reviewer_id": 2,
                },
                {
                    "id": 5,
                    "review": "reee piolaaaaaa",
                    "reviewer": "locooo",
                    "reviewer_id": 3
                },
            ],
        }
