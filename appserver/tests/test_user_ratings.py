import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.user_ratings_models import (MockUserRatingListResponse,
                                                   MockUserRatingResponse)
from tests.utils import (APPSERVER_URL, GUEST_RATING_REGEX, HOST_RATING_REGEX,
                         check_responses_equality)


@responses.activate
def test_post_host_rating(test_app, monkeypatch):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = test_rating["reviewer_id"]
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_rating)
    responses.add(
        responses.POST,
        re.compile(HOST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/users/{test_user_id}/host_ratings",
        json=test_rating,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_post_guest_rating(test_app, monkeypatch):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = 1
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_rating)
    responses.add(
        responses.POST,
        re.compile(GUEST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_ratings",
        json=test_rating,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_all_user_host_ratings(test_app):
    test_rating_list = MockUserRatingListResponse().dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_RATING_REGEX),
        json=test_rating_list,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}/host_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json["ratings"]):
        check_responses_equality(
            response_rating, test_rating_list["ratings"][i], attrs_to_test
        )


@responses.activate
def test_get_all_user_guest_ratings(test_app):
    test_rating_list = MockUserRatingListResponse().dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_RATING_REGEX),
        json=test_rating_list,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}/guest_ratings")
    response_json = response.json()

    assert response.status_code == expected_status
    for i, response_rating in enumerate(response_json["ratings"]):
        check_responses_equality(
            response_rating, test_rating_list["ratings"][i], attrs_to_test
        )


@responses.activate
def test_get_single_guest_rating(test_app):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(GUEST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_ratings/{test_rating_id}"
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_single_host_rating(test_app):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = 1
    test_rating_id = 2
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id"]

    responses.add(
        responses.GET,
        re.compile(HOST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/users/{test_user_id}/host_ratings/{test_rating_id}"
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_delete_host_rating(test_app, monkeypatch):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = test_rating["reviewer_id"]
    test_rating_id = 2
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.DELETE,
        re.compile(HOST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/users/{test_user_id}/host_ratings/{test_rating_id}",
        headers=header,
    )

    assert response.status_code == expected_status


@responses.activate
def test_delete_guest_rating(test_app, monkeypatch):
    test_rating = MockUserRatingResponse().dict()
    test_user_id = test_rating["reviewer_id"]
    test_rating_id = 2
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.DELETE,
        re.compile(GUEST_RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/users/{test_user_id}/guest_ratings/{test_rating_id}",
        headers=header,
    )

    assert response.status_code == expected_status
