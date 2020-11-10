import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.utils import MockResponse, mock_request, check_responses_equality

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


@httpretty.activate
def test_post_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.POST, mock_user_rating_response, HOST_RATING_REGEX, expected_status
    )
    response = test_app.post(f"{API_URL}/{test_user_id}/host_ratings", json=test_rating)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@httpretty.activate
def test_post_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.POST, mock_user_rating_response, GUEST_RATING_REGEX, expected_status
    )
    response = test_app.post(
        f"{API_URL}/{test_user_id}/guest_ratings", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@httpretty.activate
def test_get_all_user_host_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET,
        mock_user_rating_list_response,
        HOST_RATING_REGEX,
        expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json):
        check_responses_equality(response_rating, test_rating_list[i], attrs_to_test)


@httpretty.activate
def test_get_all_user_guest_ratings(test_app):
    mock_user_rating_list_response = MockUserRatingListResponse()
    test_rating_list = mock_user_rating_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET,
        mock_user_rating_list_response,
        GUEST_RATING_REGEX,
        expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json):
        check_responses_equality(response_rating, test_rating_list[i], attrs_to_test)


@httpretty.activate
def test_get_single_guest_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET, mock_user_rating_response, GUEST_RATING_REGEX, expected_status
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_ratings/{test_rating_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@httpretty.activate
def test_get_single_host_rating(test_app):
    mock_user_rating_response = MockUserRatingResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET, mock_user_rating_response, HOST_RATING_REGEX, expected_status
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_ratings/{test_rating_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)
