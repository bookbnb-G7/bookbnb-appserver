import httpretty
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.routes.user_router import API_URL
from tests.utils import MockResponse, mock_request, check_responses_equality

USER_REGEX = f"{API_URL}/?[0-9]*[/]?"


class MockUserResponse(MockResponse):
    def dict(self):
        return {
            "firstname": "carlito",
            "lastname": "carlos",
            "email": "carlos@aaaaaaa",
            "phonenumber": "08004444",
            "country": "CR",
            "birthdate": "9999-99-99",
        }


@httpretty.activate
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
    ]

    mock_request(httpretty.POST, mock_user_response, USER_REGEX, expected_status)
    response = test_app.post(f"{API_URL}/", json=test_user)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@httpretty.activate
def test_get_user_by_id(test_app):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()
    test_room_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "firstname",
        "lastname",
        "email",
        "phonenumber",
        "country",
        "birthdate",
    ]

    mock_request(httpretty.GET, mock_user_response, USER_REGEX, expected_status)
    response = test_app.get(f"{API_URL}/{test_room_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)
