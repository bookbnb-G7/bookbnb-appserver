import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.room_models import MockRoomResponse
from tests.mock_models.room_reviews_models import (MockReviewListResponse,
                                                   MockReviewResponse)
from tests.mock_models.user_models import MockUserResponse
from tests.utils import (APPSERVER_URL, POSTSERVER_ROOM_REGEX, REVIEW_REGEX,
                         USER_REGEX, check_responses_equality)


@responses.activate
def test_post_room_review(test_app, monkeypatch):
    test_review = MockReviewResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["review", "reviewer", "reviewer_id", "room_id", "id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_comment", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_review["reviewer_id"]
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room['id']}/reviews",
        json=test_review,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_single_room_review(test_app):
    test_review = MockReviewResponse().dict()
    test_review_id = test_review["id"]
    test_room_id = test_review["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["review", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_room_id}/reviews/{test_review_id}",
        json=test_review,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_all_room_reviews(test_app):
    mock_review_response = MockReviewListResponse()
    test_review_list = mock_review_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_compare = ["room_id"]
    room_attrs_to_compare = ["review", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(REVIEW_REGEX),
        json=mock_review_response.dict(),
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_review_list['room_id']}/reviews"
    )
    assert response.status_code == expected_status

    response_json = response.json()
    response_reviews = response_json["reviews"]
    test_reviews = test_review_list["reviews"]

    check_responses_equality(response.json(), test_review_list, attrs_to_compare)
    for i, response_review in enumerate(response_reviews):
        check_responses_equality(
            response_review, test_reviews[i], room_attrs_to_compare
        )


@responses.activate
def test_delete_room_review(test_app, monkeypatch):
    test_review = MockReviewResponse().dict()
    test_review_id = test_review["id"]
    test_room_id = test_review["room_id"]
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_review["reviewer_id"]
    )
    responses.add(
        responses.GET,
        re.compile(REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/rooms/{test_room_id}/reviews/{test_review_id}", headers=header
    )
    assert response.status_code == expected_status
