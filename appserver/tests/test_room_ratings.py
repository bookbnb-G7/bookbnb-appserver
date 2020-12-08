import re

import responses
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.utils import MockResponse, check_responses_equality

"""
from app.api.routes.room_router import API_URL
RATING_REGEX = f"{API_URL}/?[0-9]*[/]?ratings/?"


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


@responses.activate
def test_post_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_rating = mock_rating_response.dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.POST,
        re.compile(RATING_REGEX),
        json=mock_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/{test_rating['id']}/ratings", json=test_rating)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_all_room_ratings(test_app):
    mock_rating_response = MockRatingListResponse()
    test_rating_list = mock_rating_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_compare = ["room_id"]
    room_attrs_to_compare = ["rating", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(RATING_REGEX),
        json=mock_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_rating_list['room_id']}/ratings")
    assert response.status_code == expected_status

    response_json = response.json()
    response_ratings = response_json["ratings"]
    test_ratings = test_rating_list["ratings"]

    check_responses_equality(response.json(), test_rating_list, attrs_to_compare)
    for i, response_rating in enumerate(response_ratings):
        check_responses_equality(
            response_rating, test_ratings[i], room_attrs_to_compare
        )


@responses.activate
def test_get_single_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_rating = mock_rating_response.dict()
    test_rating_id = test_rating["id"]
    test_room_id = test_rating["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(RATING_REGEX),
        json=mock_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.get(
        f"{API_URL}/{test_room_id}/ratings/{test_rating_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_update_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_full_rating = mock_rating_response.dict()
    test_rating_id = 1
    test_room_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating"]
    test_rating = {attr: test_full_rating[attr] for attr in attrs_to_test}

    responses.add(
        responses.PATCH,
        re.compile(RATING_REGEX),
        json=mock_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{API_URL}/{test_room_id}/ratings/{test_rating_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_delete_room_rating(test_app):
    mock_rating_response = MockRatingResponse()
    test_rating = mock_rating_response.dict()
    test_rating_id = test_rating["id"]
    test_room_id = test_rating["room_id"]
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(RATING_REGEX),
        json=mock_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(f"{API_URL}/{test_room_id}/ratings/{test_rating_id}")
    assert response.status_code == expected_status
"""