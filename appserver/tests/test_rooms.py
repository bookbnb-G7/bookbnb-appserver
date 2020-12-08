import re

import responses
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.utils import MockResponse, check_responses_equality

"""
from app.api.routes.room_router import API_URL

POSTSERVER_ROOM_REGEX = rf"{API_URL}/?[0-9]*[/]?"


class MockRoomResponse(MockResponse):
    def dict(self):
        return {
            "type": "Apartment",
            "owner": "Carlito",
            "owner_id": 10,
            "price_per_day": 999,
            "id": 0,
            "created_at": "2020-11-10T22:51:03.539Z",
            "updated_at": "2020-11-10T22:51:03.539Z",
        }


class MockRoomListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "rooms": [
                {
                    "type": "Apartment",
                    "owner": "Carlito",
                    "owner_id": 10,
                    "price_per_day": 999,
                    "id": 0,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "type": "House",
                    "owner": "Freee",
                    "owner_id": 11,
                    "price_per_day": 123,
                    "id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }


@responses.activate
def test_create_room(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["type", "owner", "owner_id", "price_per_day"]

    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/", json=test_room)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_room, attrs_to_test)


@responses.activate
def test_get_room_by_id(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()
    test_room_id = test_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["type", "owner", "owner_id", "price_per_day"]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_response.dict(),
        status=expected_status,
    )

    response = test_app.get(f"{API_URL}/{test_room_id}")
    assert response.status_code == expected_status
    response_json = response.json()

    check_responses_equality(response.json(), test_room, attrs_to_test)
    assert response_json["id"] == test_room_id


@responses.activate
def test_get_all_rooms(test_app):
    mock_room_list_response = MockRoomListResponse()
    test_room_list = mock_room_list_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_test = ["type", "owner", "owner_id", "price_per_day"]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_list_response.dict(),
        status=expected_status,
    )

    response = test_app.get(f"{API_URL}/")
    assert response.status_code == expected_status
    response_json = response.json()

    rooms = response_json["rooms"]
    test_rooms = test_room_list["rooms"]

    check_responses_equality(response_json, test_room_list, ["amount"])

    for i, room in enumerate(rooms):
        check_responses_equality(room, test_rooms[i], attrs_to_test)


@responses.activate
def test_update_room(test_app):
    mock_room_response = MockRoomResponse()
    test_full_room = mock_room_response.dict()
    test_room_id = test_full_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["type", "price_per_day"]
    test_room = {attr: test_full_room[attr] for attr in attrs_to_test}

    responses.add(
        responses.PATCH,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(f"{API_URL}/{test_room_id}", json=test_room)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_room, attrs_to_test)


@responses.activate
def test_delete_room(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()
    test_room_id = test_room["id"]
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(f"{API_URL}/{test_room_id}")
    assert response.status_code == expected_status
"""