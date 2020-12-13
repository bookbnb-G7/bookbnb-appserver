from tests.utils import MockResponse


class MockUserReviewResponse(MockResponse):
    def dict(self):
        return {
            "review": "sisi muy lindo todo la verdad",
            "reviewer": "aaaa",
            "reviewer_id": 2,
        }


class MockUserReviewListResponse(MockResponse):
    def dict(self):
        return [
            {
                "review": "sisi muy lindo todo la verdad",
                "reviewer": "aaaa",
                "reviewer_id": 2,
            },
            {
                "review": "sese muy lindo todo la verda",
                "reviewer": "aaaa",
                "reviewer_id": 2,
            },
            {"review": "reee piolaaaaaa", "reviewer": "locooo", "reviewer_id": 3},
        ]
