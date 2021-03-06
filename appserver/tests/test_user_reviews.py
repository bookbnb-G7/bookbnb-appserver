import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.user_models import MockUserResponse
from tests.mock_models.user_reviews_models import (MockUserReviewListResponse,
                                                   MockUserReviewResponse)
from tests.utils import (APPSERVER_URL, USER_REGEX, GUEST_REVIEW_REGEX,
                         HOST_REVIEW_REGEX, check_responses_equality)


@responses.activate
def test_post_host_review(test_app, monkeypatch):
    test_review = MockUserReviewResponse().dict()
    payload = {"review": test_review["review"]}
    test_user = MockUserResponse().dict()
    test_user_id = test_review["reviewer_id"]
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_comment", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_review)

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(HOST_REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/users/{test_user_id}/host_reviews",
        json=payload,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_post_guest_review(test_app, monkeypatch):
    test_review = MockUserReviewResponse().dict()
    payload = {"review": test_review["review"]}
    test_user = MockUserResponse().dict()
    test_user_id = test_review["reviewer_id"]
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_comment", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_review)

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(GUEST_REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_reviews",
        json=payload,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_all_user_host_reviews(test_app):
    test_review_list = MockUserReviewListResponse().dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_REVIEW_REGEX),
        json=test_review_list,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}/host_reviews")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json["reviews"]):
        check_responses_equality(
            response_rating, test_review_list["reviews"][i], attrs_to_test
        )


@responses.activate
def test_get_all_user_guest_reviews(test_app):
    test_review_list = MockUserReviewListResponse().dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_REVIEW_REGEX),
        json=test_review_list,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}/guest_reviews")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json["reviews"]):
        check_responses_equality(
            response_rating, test_review_list["reviews"][i], attrs_to_test
        )


@responses.activate
def test_get_single_guest_review(test_app):
    test_review = MockUserReviewResponse().dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_reviews/{test_review_id}"
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_get_single_host_review(test_app):
    test_review = MockUserReviewResponse().dict()
    test_user_id = 1
    test_review_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["id", "review", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_REVIEW_REGEX),
        json=test_review,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/users/{test_user_id}/host_reviews/{test_review_id}"
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_review, attrs_to_test)


@responses.activate
def test_delete_host_review(test_app, monkeypatch):
    test_rating = MockUserReviewResponse().dict()
    test_user_id = test_rating["reviewer_id"]
    test_rating_id = 2
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.DELETE,
        re.compile(HOST_REVIEW_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/users/{test_user_id}/host_reviews/{test_rating_id}",
        headers=header,
    )

    assert response.status_code == expected_status


@responses.activate
def test_delete_guest_review(test_app, monkeypatch):
    test_rating = MockUserReviewResponse().dict()
    test_user_id = test_rating["reviewer_id"]
    test_rating_id = 2
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.DELETE,
        re.compile(GUEST_REVIEW_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_reviews/{test_rating_id}",
        headers=header,
    )

    assert response.status_code == expected_status
