import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.utils import MockResponse, mock_request, check_responses_equality

HOST_REVIEW_REGEX = f"{API_URL}/?[0-9]*[/]?host_reviews/?"
GUEST_REVIEW_REGEX = f"{API_URL}/?[0-9]*[/]?guest_reviews/?"


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
                "review": "sisi muy lindo todo la verdad",
                "reviewer": "aaaa",
                "reviewer_id": 2,
            },
            {"review": "reee piolaaaaaa", "reviewer": "locooo", "reviewer_id": 3},
        ]


@httpretty.activate
def test_post_host_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.POST, mock_user_review_response, HOST_REVIEW_REGEX, expected_status
    )
    response = test_app.post(f"{API_URL}/{test_user_id}/host_reviews", json=test_review)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_post_guest_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.POST, mock_user_review_response, GUEST_REVIEW_REGEX, expected_status
    )
    response = test_app.post(
        f"{API_URL}/{test_user_id}/guest_reviews", json=test_review
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_get_all_user_host_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET,
        mock_user_review_list_response,
        HOST_REVIEW_REGEX,
        expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_reviews")
    assert response.status_code == expected_status
    response_json = response.json()

    for i, response_review in enumerate(response_json):
        check_responses_equality(response_review, test_review_list[i], attrs_to_test)


@httpretty.activate
def test_get_all_user_guest_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET,
        mock_user_review_list_response,
        GUEST_REVIEW_REGEX,
        expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_reviews")
    assert response.status_code == expected_status
    response_json = response.json()

    for i, response_review in enumerate(response_json):
        check_responses_equality(response_review, test_review_list[i], attrs_to_test)


@httpretty.activate
def test_get_single_guest_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET, mock_user_review_response, GUEST_REVIEW_REGEX, expected_status
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_reviews/{test_review_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_get_single_host_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    mock_request(
        httpretty.GET, mock_user_review_response, HOST_REVIEW_REGEX, expected_status
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_reviews/{test_review_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)
