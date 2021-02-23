import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.room_models import (MockPaymentRoomResponse,
                                           MockRoomListResponse,
                                           MockRoomResponse)
from tests.mock_models.user_models import MockUserResponse
from tests.utils import (APPSERVER_URL, PAYMENT_ROOM_REGEX,
                         POSTSERVER_ROOM_REGEX, USER_REGEX,
                         POSTSERVER_RECOMENDED_REGEX, check_responses_equality)


@responses.activate
def test_create_room(test_app, monkeypatch):
    test_payment_room = MockPaymentRoomResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    test_user["id"] = test_room["owner_uuid"]
    test_room["owner"] = f"{test_user['firstname']} {test_user['lastname']}"

    expected_status = HTTP_201_CREATED
    attrs_to_test = [
        "title",
        "description",
        "type",
        "owner",
        "owner_uuid",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_room["owner_uuid"]
    )

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_ROOM_REGEX),
        json=test_payment_room,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )
    response = test_app.post(f"{APPSERVER_URL}/rooms", json=test_room, headers=header)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_room, attrs_to_test)


@responses.activate
def test_get_all_rooms(test_app):
    test_room_list = MockRoomListResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "title",
        "description",
        "type",
        "owner",
        "owner_uuid",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_list,
        status=expected_status,
    )

    response = test_app.get(f"{APPSERVER_URL}/rooms")
    assert response.status_code == expected_status
    response_json = response.json()

    rooms = response_json["rooms"]
    test_rooms = test_room_list["rooms"]

    check_responses_equality(response_json, test_room_list, ["amount"])

    for i, room in enumerate(rooms):
        check_responses_equality(room, test_rooms[i], attrs_to_test)


@responses.activate
def test_get_recomended_rooms(test_app):
    test_room_list = MockRoomListResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "title",
        "description",
        "type",
        "owner",
        "owner_uuid",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_RECOMENDED_REGEX),
        json=test_room_list,
        status=expected_status,
    )

    response = test_app.get(f"{APPSERVER_URL}/recomendations")
    assert response.status_code == expected_status
    response_json = response.json()

    rooms = response_json["rooms"]
    test_rooms = test_room_list["rooms"]

    check_responses_equality(response_json, test_room_list, ["amount"])

    for i, room in enumerate(rooms):
        check_responses_equality(room, test_rooms[i], attrs_to_test)


@responses.activate
def test_get_room_by_id(test_app):
    test_room = MockRoomResponse().dict()
    test_room_id = test_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "title",
        "description",
        "type",
        "owner",
        "owner_uuid",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )

    response = test_app.get(f"{APPSERVER_URL}/rooms/{test_room_id}")
    assert response.status_code == expected_status
    response_json = response.json()

    check_responses_equality(response.json(), test_room, attrs_to_test)
    assert response_json["id"] == test_room_id


@responses.activate
def test_update_room(test_app, monkeypatch):
    test_full_room = MockRoomResponse().dict()
    test_room_id = test_full_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "title",
        "description",
        "type",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]
    test_room = {attr: test_full_room[attr] for attr in attrs_to_test}
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_full_room["owner_uuid"]
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_full_room,
        status=expected_status,
    )
    responses.add(
        responses.PATCH,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_full_room,
        status=expected_status,
    )
    response = test_app.patch(
        f"{APPSERVER_URL}/rooms/{test_room_id}", json=test_room, headers=header
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_room, attrs_to_test)


@responses.activate
def test_delete_room(test_app, monkeypatch):
    test_room = MockRoomResponse().dict()
    test_payment_room = MockPaymentRoomResponse().dict()
    test_room_id = test_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "title",
        "description",
        "type",
        "owner",
        "owner_uuid",
        "price_per_day",
        "latitude",
        "longitude",
        "location",
        "capacity",
    ]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_room["owner_uuid"]
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(PAYMENT_ROOM_REGEX),
        json=test_payment_room,
        status=expected_status,
    )
    response = test_app.delete(f"{APPSERVER_URL}/rooms/{test_room_id}", headers=header)
    assert response.status_code == expected_status

    response_json = response.json()
    check_responses_equality(response_json, test_room, attrs_to_test)
