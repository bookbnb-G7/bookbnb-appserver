import re
import responses
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.utils import MockResponse, check_responses_equality
from app.api.routes.user_router import API_URL
"""
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


@responses.activate
def test_post_host_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.POST,
        re.compile(HOST_REVIEW_REGEX),
        json=mock_user_review_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/{test_user_id}/host_reviews", json=test_review)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_post_guest_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.POST,
        re.compile(GUEST_REVIEW_REGEX),
        json=mock_user_review_response.dict(),
        status=expected_status,
    )
    response = test_app.post(
        f"{API_URL}/{test_user_id}/guest_reviews", json=test_review
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_all_user_host_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_REVIEW_REGEX),
        json=mock_user_review_list_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_reviews")
    assert response.status_code == expected_status
    response_json = response.json()

    for i, response_review in enumerate(response_json):
        check_responses_equality(response_review, test_review_list[i], attrs_to_test)


@responses.activate
def test_get_all_user_guest_reviews(test_app):
    mock_user_review_list_response = MockUserReviewListResponse()
    test_review_list = mock_user_review_list_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_REVIEW_REGEX),
        json=mock_user_review_list_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_reviews")
    assert response.status_code == expected_status
    response_json = response.json()

    for i, response_review in enumerate(response_json):
        check_responses_equality(response_review, test_review_list[i], attrs_to_test)


@responses.activate
def test_get_single_guest_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_REVIEW_REGEX),
        json=mock_user_review_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/guest_reviews/{test_review_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_single_host_review(test_app):
    mock_user_review_response = MockUserReviewResponse()
    test_review = mock_user_review_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_REVIEW_REGEX),
        json=mock_user_review_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}/host_reviews/{test_review_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_update_host_review(test_app):
    mock_user_rating_response = MockUserReviewResponse()
    test_full_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review"]
    test_rating = {attr: test_full_rating[attr] for attr in attrs_to_test}

    responses.add(
        responses.PATCH,
        re.compile(HOST_REVIEW_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{API_URL}/{test_user_id}/host_reviews/{test_review_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_update_guest_review(test_app):
    mock_user_rating_response = MockUserReviewResponse()
    test_rating = mock_user_rating_response.dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["review"]

    responses.add(
        responses.PATCH,
        re.compile(GUEST_REVIEW_REGEX),
        json=mock_user_rating_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{API_URL}/{test_user_id}/guest_reviews/{test_review_id}", json=test_rating
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_delete_host_review(test_app):
    mock_user_response = MockUserReviewResponse()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(HOST_REVIEW_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(
        f"{API_URL}/{test_user_id}/host_reviews/{test_review_id}"
    )

    assert response.status_code == expected_status


@responses.activate
def test_delete_guest_review(test_app):
    mock_user_response = MockUserReviewResponse()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(GUEST_REVIEW_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(
        f"{API_URL}/{test_user_id}/guest_reviews/{test_review_id}"
    )

    assert response.status_code == expected_status
"""