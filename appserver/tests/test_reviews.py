import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL

REVIEW_REGEX = f"^{API_URL}/?[0-9]*[/]?reviews/?$"


class MockReviewResponse:
    @staticmethod
    def json():
        return {
            "review": "muy lindo todo",
            "reviewer": "string",
            "reviewer_id": 44,
            "id": 23,
            "room_id": 22,
        }


class MockReviewListResponse:
    @staticmethod
    def json():
        return {
            "room_id": 1,
            "reviews": [
                {
                    "review": "muy lindo todo",
                    "reviewer": "carlitos",
                    "reviewer_id": 10,
                    "id": 0,
                    "room_id": 1,
                },
                {
                    "review": "todo mal",
                    "reviewer": "remalo",
                    "reviewer_id": 666,
                    "id": 2,
                    "room_id": 1,
                },
            ],
        }


@httpretty.activate
def test_post_room_review(test_app):
    mock_review_response = MockReviewResponse()
    test_review = mock_review_response.json()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(REVIEW_REGEX),
        responses=[mock_review_response],
        status=HTTP_201_CREATED,
    )
    response = test_app.post(f"/{test_review['id']}/reviews", json=test_review)
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["room_id"] == test_review["id"]


@httpretty.activate
def test_get_all_room_reviews(test_app):
    mock_review_response = MockReviewListResponse()
    test_review_list = mock_review_response.json()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(REVIEW_REGEX),
        responses=[mock_review_response],
        status=HTTP_200_OK,
    )
    response = test_app.get(f"/{test_review_list['room_id']}/reviews")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    response_ratings = response_json["reviews"]
    test_ratings = test_review_list["reviews"]

    assert response_json["room_id"] == test_review_list["room_id"]
    for response_rating, i in enumerate(response_ratings):
        assert response_rating["review"] == test_ratings[i]["review"]
        assert response_rating["reviewer"] == test_ratings[i]["reviewer"]
        assert response_rating["reviewer_id"] == test_ratings[i]["reviewer_id"]


@httpretty.activate
def test_get_single_room_rating(test_app):
    mock_review_response = MockReviewResponse()
    test_review = mock_review_response.json()
    test_room_id = test_review["room_id"]
    test_review_id = test_review["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(REVIEW_REGEX),
        responses=[mock_review_response],
        status=HTTP_200_OK,
    )
    response = test_app.get(f"/{test_room_id}/reviews/{test_review_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == test_review_id
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["room_id"] == test_room_id
