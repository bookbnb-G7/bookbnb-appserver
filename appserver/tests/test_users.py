import re
import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.conftest import MockResponse

USER_REGEX = f"{API_URL}/?[0-9]*[/]?"


class MockUserResponse(MockResponse):
    def dict(self):
        return {
            "id": 2,
            "firstname": "carlito",
            "lastname": "carlos",
            "email": "carlos@aaaaaaa",
            "phonenumber": "08004444",
            "country": "CR",
            "birthdate": "9999-99-99",
            "updatedAt": "2020-11-03T20:05:10.673Z",
            "createdAt": "2020-11-03T20:05:10.673Z",
        }


@httpretty.activate
def test_create_room(test_app):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()

    httpretty.register_uri(
        httpretty.POST,
        re.compile(USER_REGEX),
        responses=[
            httpretty.Response(body=mock_user_response.json(), status=HTTP_201_CREATED)
        ],
    )
    response = test_app.post(f"{API_URL}/", json=test_user)
    response_json = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert response_json["id"] == test_user["id"]
    assert response_json["firstname"] == test_user["firstname"]
    assert response_json["lastname"] == test_user["lastname"]
    assert response_json["email"] == test_user["email"]
    assert response_json["phonenumber"] == test_user["phonenumber"]
    assert response_json["country"] == test_user["country"]
    assert response_json["birthdate"] == test_user["birthdate"]
    assert response_json["updatedAt"] == test_user["updatedAt"]
    assert response_json["createdAt"] == test_user["createdAt"]


@httpretty.activate
def test_get_room_by_id(test_app):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()

    httpretty.register_uri(
        httpretty.GET,
        re.compile(USER_REGEX),
        responses=[httpretty.Response(body=mock_user_response.json())],
    )
    test_room_id = test_user["id"]
    response = test_app.get(f"{API_URL}/{test_room_id}")
    response_json = response.json()

    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == test_user["id"]
    assert response_json["firstname"] == test_user["firstname"]
    assert response_json["lastname"] == test_user["lastname"]
    assert response_json["email"] == test_user["email"]
    assert response_json["phonenumber"] == test_user["phonenumber"]
    assert response_json["country"] == test_user["country"]
    assert response_json["birthdate"] == test_user["birthdate"]
    assert response_json["updatedAt"] == test_user["updatedAt"]
    assert response_json["createdAt"] == test_user["createdAt"]
