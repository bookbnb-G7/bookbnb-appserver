import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.conftest import MockResponse

HOST_RATING_REGEX = f"{API_URL}/?[0-9]*[/]?host_ratings/?"
GUEST_RATING_REGEX = f"{API_URL}/?[0-9]*[/]?guest_ratings/?"


class MockUserRatingResponse(MockResponse):
    def dict(self):
        return {
            "id": 1,
            "userId": 1,
            "rating": 5,
            "reviewer": "aaaa",
            "reviewer_id": "2",
            "updatedAt": "2020-11-03T21:42:11.876Z",
            "createdAt": "2020-11-03T21:42:11.876Z",
        }


class MockUserRatingListResponse(MockResponse):
    def dict(self):
        return [
            {
                "id": 1,
                "rating": 5,
                "reviewer": "aaaa",
                "reviewer_id": "2",
                "createdAt": "2020-11-03T21:42:11.876Z",
                "updatedAt": "2020-11-03T21:42:11.876Z",
                "userId": 1,
            },
            {
                "id": 2,
                "rating": 3,
                "reviewer": "jon",
                "reviewer_id": "4",
                "createdAt": "2020-11-03T21:43:04.692Z",
                "updatedAt": "2020-11-03T21:43:04.692Z",
                "userId": 1,
            },
            {
                "id": 3,
                "rating": 1,
                "reviewer": "malaonda",
                "reviewer_id": "5",
                "createdAt": "2020-11-03T21:43:16.869Z",
                "updatedAt": "2020-11-03T21:43:16.869Z",
                "userId": 1,
            },
        ]


@httpretty.activate
def test_post_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(HOST_RATING_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_rating_response.json(), status=HTTP_201_CREATED
            )
        ],
    )
    response = test_app.post(
        f"{API_URL}/{test_rating['userId']}/host_ratings", json=test_rating
    )
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["createdAt"] == test_rating["createdAt"]
    assert response_json["updatedAt"] == test_rating["updatedAt"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["userId"] == test_rating["userId"]
    assert response_json["id"] == test_rating["id"]


@httpretty.activate
def test_post_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(GUEST_RATING_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_rating_response.json(), status=HTTP_201_CREATED
            )
        ],
    )
    response = test_app.post(
        f"{API_URL}/{test_rating['id']}/guest_ratings", json=test_rating
    )
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["createdAt"] == test_rating["createdAt"]
    assert response_json["updatedAt"] == test_rating["updatedAt"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["userId"] == test_rating["userId"]
    assert response_json["id"] == test_rating["id"]


@httpretty.activate
def test_get_all_user_host_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(HOST_RATING_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_rating_list_response.json(), status=HTTP_200_OK
            )
        ],
    )
    response = test_app.get(f"{API_URL}/{test_rating_list[0]['userId']}/host_ratings")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    for i, response_rating in enumerate(response_json):
        assert response_rating["rating"] == test_rating_list[i]["rating"]
        assert response_rating["reviewer"] == test_rating_list[i]["reviewer"]
        assert response_rating["createdAt"] == test_rating_list[i]["createdAt"]
        assert response_rating["updatedAt"] == test_rating_list[i]["updatedAt"]
        assert response_rating["reviewer_id"] == test_rating_list[i]["reviewer_id"]
        assert response_rating["userId"] == test_rating_list[i]["userId"]
        assert response_rating["id"] == test_rating_list[i]["id"]


@httpretty.activate
def test_get_all_user_guest_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(GUEST_RATING_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_rating_list_response.json(), status=HTTP_200_OK
            )
        ],
    )
    response = test_app.get(f"{API_URL}/{test_rating_list[0]['userId']}/guest_ratings")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    for i, response_rating in enumerate(response_json):
        assert response_rating["rating"] == test_rating_list[i]["rating"]
        assert response_rating["reviewer"] == test_rating_list[i]["reviewer"]
        assert response_rating["createdAt"] == test_rating_list[i]["createdAt"]
        assert response_rating["updatedAt"] == test_rating_list[i]["updatedAt"]
        assert response_rating["reviewer_id"] == test_rating_list[i]["reviewer_id"]
        assert response_rating["userId"] == test_rating_list[i]["userId"]
        assert response_rating["id"] == test_rating_list[i]["id"]


@httpretty.activate
def test_get_single_guest_rating(test_app):
    mock_rating_response = MockUserRatingResponse()
    test_rating = mock_rating_response.dict()
    test_user_id = test_rating["userId"]
    test_rating_id = test_rating["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(GUEST_RATING_REGEX),
        responses=[
            httpretty.Response(body=mock_rating_response.json(), status=HTTP_200_OK)
        ],
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_ratings/{test_rating_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["createdAt"] == test_rating["createdAt"]
    assert response_json["updatedAt"] == test_rating["updatedAt"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["userId"] == test_rating["userId"]
    assert response_json["id"] == test_rating["id"]


@httpretty.activate
def test_get_single_host_rating(test_app):
    mock_rating_response = MockUserRatingResponse()
    test_rating = mock_rating_response.dict()
    test_user_id = test_rating["userId"]
    test_rating_id = test_rating["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(HOST_RATING_REGEX),
        responses=[
            httpretty.Response(body=mock_rating_response.json(), status=HTTP_200_OK)
        ],
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_ratings/{test_rating_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["rating"] == test_rating["rating"]
    assert response_json["reviewer"] == test_rating["reviewer"]
    assert response_json["createdAt"] == test_rating["createdAt"]
    assert response_json["updatedAt"] == test_rating["updatedAt"]
    assert response_json["reviewer_id"] == test_rating["reviewer_id"]
    assert response_json["userId"] == test_rating["userId"]
    assert response_json["id"] == test_rating["id"]
