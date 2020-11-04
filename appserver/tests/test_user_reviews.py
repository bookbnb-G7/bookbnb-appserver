import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.conftest import MockResponse

HOST_REVIEW_REGEX = f"{API_URL}/?[0-9]*[/]?host_reviews/?"
GUEST_REVIEW_REGEX = f"{API_URL}/?[0-9]*[/]?guest_reviews/?"


class MockUserReviewResponse(MockResponse):
    def dict(self):
        return {
            "id": 1,
            "review": "sisi muy lindo todo la verdad",
            "reviewer": "aaaa",
            "reviewer_id": "2",
            "createdAt": "2020-11-03T21:24:06.736Z",
            "updatedAt": "2020-11-03T21:24:06.736Z",
            "userId": 1,
        }


class MockUserReviewListResponse(MockResponse):
    def dict(self):
        return [
            {
                "id": 1,
                "review": "sisi muy lindo todo la verdad",
                "reviewer": "aaaa",
                "reviewer_id": "2",
                "createdAt": "2020-11-03T21:24:06.736Z",
                "updatedAt": "2020-11-03T21:24:06.736Z",
                "userId": 1,
            },
            {
                "id": 2,
                "review": "sisi muy lindo todo la verdad",
                "reviewer": "aaaa",
                "reviewer_id": "2",
                "createdAt": "2020-11-03T21:26:32.654Z",
                "updatedAt": "2020-11-03T21:26:32.654Z",
                "userId": 1,
            },
            {
                "id": 3,
                "review": "reee piolaaaaaa",
                "reviewer": "locooo",
                "reviewer_id": "3",
                "createdAt": "2020-11-03T21:31:26.003Z",
                "updatedAt": "2020-11-03T21:31:26.003Z",
                "userId": 1,
            },
        ]


@httpretty.activate
def test_post_host_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(HOST_REVIEW_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_review_response.json(), status=HTTP_201_CREATED
            )
        ],
    )
    response = test_app.post(
        f"{API_URL}/{test_review['userId']}/host_reviews", json=test_review
    )
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["createdAt"] == test_review["createdAt"]
    assert response_json["updatedAt"] == test_review["updatedAt"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["userId"] == test_review["userId"]
    assert response_json["id"] == test_review["id"]


@httpretty.activate
def test_post_guest_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(GUEST_REVIEW_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_review_response.json(), status=HTTP_201_CREATED
            )
        ],
    )
    response = test_app.post(
        f"{API_URL}/{test_review['id']}/guest_reviews", json=test_review
    )
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["createdAt"] == test_review["createdAt"]
    assert response_json["updatedAt"] == test_review["updatedAt"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["userId"] == test_review["userId"]
    assert response_json["id"] == test_review["id"]


@httpretty.activate
def test_get_all_user_host_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(HOST_REVIEW_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_review_list_response.json(), status=HTTP_200_OK
            )
        ],
    )
    response = test_app.get(f"{API_URL}/{test_review_list[0]['userId']}/host_reviews")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    for i, response_rating in enumerate(response_json):
        assert response_rating["review"] == test_review_list[i]["review"]
        assert response_rating["reviewer"] == test_review_list[i]["reviewer"]
        assert response_rating["createdAt"] == test_review_list[i]["createdAt"]
        assert response_rating["updatedAt"] == test_review_list[i]["updatedAt"]
        assert response_rating["reviewer_id"] == test_review_list[i]["reviewer_id"]
        assert response_rating["userId"] == test_review_list[i]["userId"]
        assert response_rating["id"] == test_review_list[i]["id"]


@httpretty.activate
def test_get_all_user_guest_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(GUEST_REVIEW_REGEX),
        responses=[
            httpretty.Response(
                body=mock_user_review_list_response.json(), status=HTTP_200_OK
            )
        ],
    )
    response = test_app.get(f"{API_URL}/{test_review_list[0]['userId']}/guest_reviews")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK

    for i, response_rating in enumerate(response_json):
        assert response_rating["review"] == test_review_list[i]["review"]
        assert response_rating["reviewer"] == test_review_list[i]["reviewer"]
        assert response_rating["createdAt"] == test_review_list[i]["createdAt"]
        assert response_rating["updatedAt"] == test_review_list[i]["updatedAt"]
        assert response_rating["reviewer_id"] == test_review_list[i]["reviewer_id"]
        assert response_rating["userId"] == test_review_list[i]["userId"]
        assert response_rating["id"] == test_review_list[i]["id"]


@httpretty.activate
def test_get_single_guest_review(test_app):
    mock_review_response = MockUserReviewResponse()
    test_review = mock_review_response.dict()
    test_user_id = test_review["userId"]
    test_review_id = test_review["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(GUEST_REVIEW_REGEX),
        responses=[
            httpretty.Response(body=mock_review_response.json(), status=HTTP_200_OK)
        ],
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_reviews/{test_review_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["createdAt"] == test_review["createdAt"]
    assert response_json["updatedAt"] == test_review["updatedAt"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["userId"] == test_review["userId"]
    assert response_json["id"] == test_review["id"]


@httpretty.activate
def test_get_single_host_review(test_app):
    mock_review_response = MockUserReviewResponse()
    test_review = mock_review_response.dict()
    test_user_id = test_review["userId"]
    test_review_id = test_review["id"]

    httpretty.register_uri(
        httpretty.GET,
        re.compile(HOST_REVIEW_REGEX),
        responses=[
            httpretty.Response(body=mock_review_response.json(), status=HTTP_200_OK)
        ],
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_reviews/{test_review_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["review"] == test_review["review"]
    assert response_json["reviewer"] == test_review["reviewer"]
    assert response_json["createdAt"] == test_review["createdAt"]
    assert response_json["updatedAt"] == test_review["updatedAt"]
    assert response_json["reviewer_id"] == test_review["reviewer_id"]
    assert response_json["userId"] == test_review["userId"]
    assert response_json["id"] == test_review["id"]
