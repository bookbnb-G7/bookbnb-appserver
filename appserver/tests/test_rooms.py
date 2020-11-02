import json
import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL

ROOM_REGEX = f"^{API_URL}/?[0-9]*[/]?$"


class MockRoomResponse:
    @staticmethod
    def json():
        return {
            "type": "Apartment",
            "owner": "Carlito",
            "owner_id": 10,
            "price_per_day": 999,
            "id": 0,
        }


def request_callback(method, uri, headers):
    body = json.dumps(MockRoomResponse().json())
    return 201, headers, body


@httpretty.activate
def test_create_room(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.json()

    httpretty.register_uri(
        httpretty.POST,
        f"{API_URL}/",
        responses=[httpretty.Response(body=json.dumps(test_room), status=201)],
    )
    httpretty.enable()
    response = test_app.post(f"{API_URL}/", json=test_room)
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["type"] == test_room["type"]
    assert response_json["owner"] == test_room["owner"]
    assert response_json["owner_id"] == test_room["owner_id"]
    assert response_json["price_per_day"] == test_room["price_per_day"]


@httpretty.activate
def test_get_room_by_id(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.json()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(ROOM_REGEX),
        responses=[httpretty.Response(body=request_callback)],
    )
    test_room_id = test_room["id"]
    response = test_app.get(f"/{test_room_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == test_room_id
    assert response_json["type"] == test_room["type"]
    assert response_json["owner"] == test_room["owner_id"]
    assert response_json["owner_id"] == test_room["owner_id"]
    assert response_json["price_per_day"] == test_room["price_per_day"]
