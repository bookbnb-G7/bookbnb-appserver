import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL

RATING_REGEX = f"^{API_URL}/?[0-9]*[/]?ratings/?$"


class MockRatingResponse:
    @staticmethod
    def json():
        return {
            "rating": 4,
            "reviewer": "string",
            "reviewer_id": 44,
            "id": 23,
            "room_id": 22,
        }


class MockRatingListResponse:
    @staticmethod
    def json():
        return {
            "room_id": 1,
            "ratings": [
                {
                    "rating": 5,
                    "reviewer": "carlito",
                    "reviewer_id": 0,
                    "id": 0,
                    "room_id": 1,
                },
                {
                    "rating": 0,
                    "reviewer": "remalo",
                    "reviewer_id": 666,
                    "id": 2,
                    "room_id": 1,
                },
            ],
        }


@httpretty.activate
def test_post_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_rating = mock_rating_response.json()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(RATING_REGEX),
        responses=[mock_rating_response],
        status=HTTP_201_CREATED,
    )
    response = test_app.post(f"/{test_rating['id']}/ratings", json=test_rating)
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["room_id"] == test_rating["id"]


@httpretty.activate
def test_get_all_room_ratings(test_app):
    mock_rating_response = MockRatingListResponse()
    test_rating_list = mock_rating_response.json()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(RATING_REGEX),
        responses=[mock_rating_response],
        status=HTTP_200_OK,
    )
    response = test_app.get(f"/{test_rating_list['room_id']}/ratings")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    response_ratings = response_json["ratings"]
    test_ratings = test_rating_list["ratings"]

    assert response_json["room_id"] == test_rating_list["room_id"]
    for response_rating, i in enumerate(response_ratings):
        assert response_rating["rating"] == test_ratings[i]["rating"]
        assert response_rating["reviewer"] == test_ratings[i]["reviewer"]
        assert response_rating["reviewer_id"] == test_ratings[i]["reviewer_id"]


@httpretty.activate
def test_get_single_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_rating = mock_rating_response.json()
    test_room_id = test_rating["room_id"]
    test_rating_id = test_rating["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(RATING_REGEX),
        responses=[mock_rating_response],
        status=HTTP_200_OK,
    )
    response = test_app.get(f"/{test_room_id}/ratings/{test_rating_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == test_rating_id
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["room_id"] == test_room_id
