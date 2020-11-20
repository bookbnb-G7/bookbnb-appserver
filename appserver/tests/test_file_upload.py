import httpretty
from firebase_admin import storage
from starlette.status import HTTP_200_OK
from tests.test_users import MockUserResponse, USER_REGEX
from tests.utils import mock_request, check_responses_equality

API_URL = "https://bookbnb-appserver.herokuapp.com"


class MockFirebaseBlob:
    def __init__(self):
        self.public_url = "www.google.com"

    def upload_from_file(self, file):
        pass

    def make_public(self):
        pass


class MockFirebaseBucketResponse:
    def blob(self, name):
        return MockFirebaseBlob()


@httpretty.activate
def test_change_profile_picture(test_app, monkeypatch):
    mock_user_response = MockUserResponse()
    test_user = mock_user_response.dict()
    test_user_id = 1
    test_files = {"file": ("test_image.png", b"laimageeennnrefake")}
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

    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    mock_request(httpretty.PATCH, mock_user_response, USER_REGEX, expected_status)
    response = test_app.post(
        f"{API_URL}/upload_profile_picture/{test_user_id}", files=test_files
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)
