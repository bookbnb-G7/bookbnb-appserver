import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL
from tests.conftest import MockResponse

ROOM_REGEX = f"{API_URL}/?[0-9]*[/]?"


class MockRoomResponse(MockResponse):
    def dict(self):
        return {
            "type": "Apartment",
            "owner": "Carlito",
            "owner_id": 10,
            "price_per_day": 999,
            "id": 0,
        }


@httpretty.activate
def test_create_room(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(ROOM_REGEX),
        responses=[
            httpretty.Response(body=mock_room_response.json(), status=HTTP_201_CREATED)
        ],
    )
    response = test_app.post(f"{API_URL}/", json=test_room)
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["type"] == test_room["type"]
    assert response_json["owner"] == test_room["owner"]
    assert int(response_json["owner_id"]) == test_room["owner_id"]
    assert int(response_json["price_per_day"]) == test_room["price_per_day"]


@httpretty.activate
def test_get_room_by_id(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(ROOM_REGEX),
        responses=[httpretty.Response(body=mock_room_response.json())],
    )
    test_room_id = test_room["id"]
    response = test_app.get(f"{API_URL}/{test_room_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == test_room_id
    assert response_json["type"] == test_room["type"]
    assert response_json["owner"] == test_room["owner"]
    assert int(response_json["owner_id"]) == test_room["owner_id"]
    assert int(response_json["price_per_day"]) == test_room["price_per_day"]
