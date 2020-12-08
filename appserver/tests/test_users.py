import re

import responses
from app.api.routes.user_router import API_URL
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.utils import MockResponse, check_responses_equality

"""
USER_REGEX = rf"{API_URL}/?[0-9]*[/]?"


class MockUserResponse(MockResponse):
    def dict(self):
        return {
            "firstname": "carlito",
            "lastname": "carlos",
            "email": "carlos@aaaaaaa",
            "phonenumber": "08004444",
            "country": "CR",
            "birthdate": "9999-99-99",
            "photo": "https://www.cmtv.com.ar/imagenes_artistas/70.jpg?Chayanne",
        }


class MockUserListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "users": [
                {
                    "firstname": "carlito",
                    "lastname": "carlos",
                    "email": "carlos@aaaaaaa",
                    "phonenumber": "08004444",
                    "country": "CR",
                    "birthdate": "9999-99-99",
                    "photo": "otrolinkkkk",
                },
                {
                    "firstname": "elmer",
                    "lastname": "figueroa",
                    "email": "carlos@eeee",
                    "phonenumber": "08004444",
                    "country": "CHY",
                    "birthdate": "9999-99-99",
                    "photo": "unlinkkkkk",
                },
            ],
        }


@responses.activate
def test_create_user(test_app):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = [
        "firstname",
        "lastname",
        "email",
        "phonenumber",
        "country",
        "birthdate",
        "photo",
    ]

    responses.add(
        responses.POST,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/", json=test_user)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_get_user_by_id(test_app):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "firstname",
        "lastname",
        "email",
        "phonenumber",
        "country",
        "birthdate",
        "photo",
    ]

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/{test_user_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_edit_user(test_app):
    mock_user_response = MockUserResponse()
    test_full_user = mock_user_response.dict()
    test_room_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = ["firstname", "lastname", "email", "phonenumber"]
    test_user = {attr: test_full_user[attr] for attr in attrs_to_test}

    responses.add(
        responses.PATCH,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(f"{API_URL}/{test_room_id}", json=test_user)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_delete_user(test_app):
    mock_user_response = MockUserResponse()
    test_room_id = 1
    expected_status = HTTP_200_OK

    responses.add(
        responses.DELETE,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.delete(f"{API_URL}/{test_room_id}")

    assert response.status_code == expected_status


@responses.activate
def test_get_all_users(test_app):
    mock_user_list_response = MockUserListResponse()
    test_user_list = mock_user_list_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "firstname",
        "lastname",
        "email",
        "phonenumber",
        "country",
        "birthdate",
        "photo",
    ]

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=mock_user_list_response.dict(),
        status=expected_status,
    )
    response = test_app.get(f"{API_URL}/")
    response_json = response.json()

    assert response.status_code == expected_status
    check_responses_equality(response_json, test_user_list, ["amount"])

    test_users = test_user_list["users"]
    response_users = response_json["users"]

    for i, user in enumerate(response_users):
        check_responses_equality(user, test_users[i], attrs_to_test)
"""