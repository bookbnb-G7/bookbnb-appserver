import re
import responses
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.utils import MockResponse, check_responses_equality
from app.api.routes.user_router import API_URL
"""
HOST_RATING_REGEX = f"{API_URL}/?[0-9]*[/]?host_ratings/?"
GUEST_RATING_REGEX = f"{API_URL}/?[0-9]*[/]?guest_ratings/?"


class MockUserRatingResponse(MockResponse):
    def dict(self):
        return {
            "id": 1,
            "userId": 1,
            "rating": 5,
            "reviewer": "aaaa",
            "reviewer_id": 2,
        }


class MockUserRatingListResponse(MockResponse):
    def dict(self):
        return [
            {
                "id": 1,
                "rating": 5,
                "reviewer": "aaaa",
                "reviewer_id": 2,
                "userId": 1,
            },
            {
                "id": 2,
                "rating": 3,
                "reviewer": "jon",
                "reviewer_id": 4,
                "userId": 1,
            },
            {
                "id": 3,
                "rating": 1,
                "reviewer": "malaonda",
                "reviewer_id": 5,
                "userId": 1,
            },
        ]


@responses.activate
def test_post_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.POST,
        re.compile(HOST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/{test_user_id}/host_ratings", json=test_rating)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_post_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.POST,
        re.compile(GUEST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.post(
        f"{API_URL}/{test_user_id}/guest_ratings", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_all_user_host_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_RATING_REGEX),
        json=mock_user_rating_list_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json):
        check_responses_equality(response_rating, test_rating_list[i], attrs_to_test)


@responses.activate
def test_get_all_user_guest_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_RATING_REGEX),
        json=mock_user_rating_list_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json):
        check_responses_equality(response_rating, test_rating_list[i], attrs_to_test)


@responses.activate
def test_get_single_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_ratings/{test_rating_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_single_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_ratings/{test_rating_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_update_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_full_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating"]
    test_rating = {attr: test_full_rating[attr] for attr in attrs_to_test}

    responses.add(
        responses.PATCH,
        re.compile(HOST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{API_URL}/{test_user_id}/host_ratings/{test_rating_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_update_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating"]

    responses.add(
        responses.PATCH,
        re.compile(GUEST_RATING_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{API_URL}/{test_user_id}/guest_ratings/{test_rating_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_delete_host_review(test_app):
    mock_user_response = MockUserRatingResponse()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(HOST_RATING_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(
        f"{API_URL}/{test_user_id}/host_ratings/{test_review_id}"
    )

    assert response.status_code == expected_status


@responses.activate
def test_delete_guest_review(test_app):
    mock_user_response = MockUserRatingResponse()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(GUEST_RATING_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(
        f"{API_URL}/{test_user_id}/guest_ratings/{test_review_id}"
    )

    assert response.status_code == expected_status
"""