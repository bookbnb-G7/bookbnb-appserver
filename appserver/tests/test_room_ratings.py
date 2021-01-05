import re
import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.room_models import MockRoomResponse
from tests.mock_models.room_ratings_models import (MockRatingListResponse,
                                                   MockRatingResponse)
from tests.mock_models.user_models import MockUserResponse
from tests.utils import (APPSERVER_URL, POSTSERVER_ROOM_REGEX, RATING_REGEX,
                         USER_REGEX, check_responses_equality)


@responses.activate
def test_post_room_rating(test_app, monkeypatch):
    test_rating = MockRatingResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["rating", "reviewer", "reviewer_id", "room_id", "id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_comment", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_rating["reviewer_id"]
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
        re.compile(RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_rating['id']}/ratings",
        json=test_rating,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_single_room_rating(test_app):
    test_rating = MockRatingResponse().dict()
    test_rating_id = test_rating["id"]
    test_room_id = test_rating["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["rating", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_room_id}/ratings/{test_rating_id}",
        json=test_rating,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_rating, attrs_to_test)


@responses.activate
def test_get_all_room_ratings(test_app):
    test_rating_list = MockRatingListResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_compare = ["room_id"]
    room_attrs_to_compare = ["rating", "reviewer", "reviewer_id", "room_id", "id"]

    responses.add(
        responses.GET,
        re.compile(RATING_REGEX),
        json=test_rating_list,
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_rating_list['room_id']}/ratings"
    )
    assert response.status_code == expected_status

    response_json = response.json()
    response_ratings = response_json["ratings"]
    test_ratings = test_rating_list["ratings"]

    check_responses_equality(response.json(), test_rating_list, attrs_to_compare)
    for i, response_rating in enumerate(response_ratings):
        check_responses_equality(
            response_rating, test_ratings[i], room_attrs_to_compare
        )


@responses.activate
def test_delete_room_rating(test_app, monkeypatch):
    test_rating = MockRatingResponse().dict()
    test_rating_id = test_rating["id"]
    test_room_id = test_rating["room_id"]
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_rating["reviewer_id"]
    )
    responses.add(
        responses.GET,
        re.compile(RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(RATING_REGEX),
        json=test_rating,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/rooms/{test_room_id}/ratings/{test_rating_id}", headers=header
    )
    assert response.status_code == expected_status
