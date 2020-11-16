import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL
from tests.utils import MockResponse, mock_request, check_responses_equality

REVIEW_REGEX = f"{API_URL}/?[0-9]*[/]?reviews/?"


class MockReviewResponse(MockResponse):
    def dict(self):
        return {
            "review": "muy lindo todo",
            "reviewer": "string",
            "reviewer_id": 44,
            "id": 23,
            "room_id": 22,
            "created_at": "2020-11-10T22:51:03.539Z",
            "updated_at": "2020-11-10T22:51:03.539Z",
        }


class MockReviewListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 1,
            "reviews": [
                {
                    "review": "muy lindo todo",
                    "reviewer": "carlitos",
                    "reviewer_id": 10,
                    "id": 0,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "review": "todo mal",
                    "reviewer": "remalo",
                    "reviewer_id": 666,
                    "id": 2,
                    "room_id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }


@httpretty.activate
def test_post_room_review(test_app):
    mock_review_response = MockReviewResponse()
    test_review = mock_review_response.dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id", "room_id", "id"]

    mock_request(httpretty.POST, mock_review_response, REVIEW_REGEX, expected_status)
    response = test_app.post(f"{API_URL}/{test_review['id']}/reviews", json=test_review)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_get_all_room_reviews(test_app):
    mock_review_response = MockReviewListResponse()
    test_review_list = mock_review_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_compare = ["room_id"]
    room_attrs_to_compare = ["review", "reviewer", "reviewer_id", "room_id", "id"]

    mock_request(httpretty.GET, mock_review_response, REVIEW_REGEX, expected_status)
    response = test_app.get(f"{API_URL}/{test_review_list['room_id']}/reviews")
    assert response.status_code == expected_status

    response_json = response.json()
    response_reviews = response_json["reviews"]
    test_reviews = test_review_list["reviews"]

    check_responses_equality(response.json(), test_review_list, attrs_to_compare)
    for i, response_review in enumerate(response_reviews):
        check_responses_equality(
            response_review, test_reviews[i], room_attrs_to_compare
        )


@httpretty.activate
def test_get_single_room_review(test_app):
    mock_review_response = MockReviewResponse()
    test_review = mock_review_response.dict()
    test_review_id = test_review["id"]
    test_room_id = test_review["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id", "room_id", "id"]

    mock_request(httpretty.GET, mock_review_response, REVIEW_REGEX, expected_status)
    response = test_app.get(f"{API_URL}/{test_room_id}/reviews/{test_review_id}")
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_update_room_review(test_app):
    mock_review_response = MockReviewResponse()
    test_full_review = mock_review_response.dict()
    test_review_id = 1
    test_room_id = 2
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review"]
    test_review = {attr: test_full_review[attr] for attr in attrs_to_test}

    mock_request(httpretty.PATCH, mock_review_response, REVIEW_REGEX, expected_status)
    response = test_app.patch(
        f"{API_URL}/{test_room_id}/reviews/{test_review_id}", json=test_review
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@httpretty.activate
def test_delete_room_review(test_app):
    mock_review_response = MockReviewResponse()
    test_review = mock_review_response.dict()
    test_review_id = test_review["id"]
    test_room_id = test_review["room_id"]
    expected_status = HTTP_200_OK

    mock_request(httpretty.DELETE, mock_review_response, REVIEW_REGEX, expected_status)
    response = test_app.delete(f"{API_URL}/{test_room_id}/reviews/{test_review_id}")
    assert response.status_code == expected_status
