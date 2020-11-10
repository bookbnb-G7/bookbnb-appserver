import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.room_router import API_URL
from tests.utils import MockResponse, mock_request, check_responses_equality


ROOM_REGEX = f"{API_URL}/?[0-9]*[/]?"


class MockRoomResponse(MockResponse):
    def dict(self):
        return {
            "type": "Apartment",
            "owner": "Carlito",
            "owner_id": "10",
            "price_per_day": 999,
            "id": 0,
        }


@httpretty.activate
def test_create_room(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["type", "owner", "owner_id", "price_per_day"]

    mock_request(httpretty.POST, mock_room_response, ROOM_REGEX, expected_status)
    response = test_app.post(f"{API_URL}/", json=test_room)
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_room, attrs_to_test)


@httpretty.activate
def test_get_room_by_id(test_app):
    mock_room_response = MockRoomResponse()
    test_room = mock_room_response.dict()
    test_room_id = test_room["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["type", "owner", "owner_id", "price_per_day"]

    mock_request(httpretty.GET, mock_room_response, ROOM_REGEX, expected_status)

    response = test_app.get(f"{API_URL}/{test_room_id}")
    assert response.status_code == expected_status
    response_json = response.json()

    check_responses_equality(response.json(), test_room, attrs_to_test)
    assert response_json["id"] == test_room_id
