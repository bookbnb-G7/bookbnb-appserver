import re

import responses
from firebase_admin import storage
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.test_rooms import POSTSERVER_ROOM_REGEX
from tests.test_users import USER_REGEX, MockUserResponse
from tests.utils import MockResponse, check_responses_equality


API_URL = "https://bookbnb-appserver.herokuapp.com"
APPSERVER_ROOM_REGEX = fr"{API_URL}/rooms/?[0-9]*[/]?"


class MockFirebaseBlob:
    def __init__(self):
        self.public_url = "www.google.cHTTPExceptionom"

    def upload_from_file(self, file):
        pass

    def make_public(self):
        pass

    def delete(self):
        pass


class MockFirebaseBucketResponse:
    def blob(self, name):
        return MockFirebaseBlob()

    def get_blob(self, blob_name):
        return MockFirebaseBlob()


class MockRoomPhotoUploadResponse(MockResponse):
    def dict(self):
        return {
            "url": "urlpiola",
            "firebase_id": 0,
            "id": 0,
            "room_id": 8,
            "created_at": "2020-12-01T19:00:00.033000+00:00",
            "updated_at": "2020-12-01T19:00:00.033000+00:00",
        }


class MockRoomPhotoList(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 8,
            "room_photos": [
                {
                    "url": "urlpiola",
                    "firebase_id": 0,
                    "id": 0,
                    "room_id": 8,
                    "created_at": "2020-12-01T19:00:00.033000+00:00",
                    "updated_at": "2020-12-01T19:00:00.033000+00:00",
                },
                {
                    "url": "otraurl",
                    "firebase_id": 1,
                    "id": 1,
                    "room_id": 8,
                    "created_at": "2020-12-02T19:00:00.033000+00:00",
                    "updated_at": "2020-12-02T19:00:00.033000+00:00",
                },
            ],
        }


def upload_photo(test_app, test_room_id):
    test_files = {"file": ("test_image.png", b"laimageeennnrefake")}
    test_app.post(f"{API_URL}/rooms/{test_room_id}/photos", files=test_files)


@responses.activate
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
    responses.add(
        responses.PATCH,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(f"{API_URL}/users/{test_user_id}/photo", files=test_files)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_upload_room_photo(test_app, monkeypatch):
    mock_room_photo_response = MockRoomPhotoUploadResponse()
    test_room_photo = mock_room_photo_response.dict()
    test_room_id = test_room_photo["room_id"]
    test_files = {"file": ("test_image.png", b"laimageeennnrefake")}
    expected_status = HTTP_201_CREATED
    attrs_to_test = [
        "url",
        "firebase_id",
        "id",
        "room_id",
        "created_at",
        "updated_at",
    ]

    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_photo_response.dict(),
        status=expected_status,
    )
    response = test_app.post(f"{API_URL}/rooms/{test_room_id}/photos", files=test_files)
    response_json = response.json()

    assert response.status_code == expected_status
    check_responses_equality(response_json, test_room_photo, attrs_to_test)


@responses.activate
def test_get_all_room_photos(test_app, monkeypatch):
    mock_room_photos = MockRoomPhotoList().dict()
    test_room_id = mock_room_photos["room_id"]
    expected_status = HTTP_200_OK
    list_attrs_to_test = ["amount", "room_id"]
    attrs_to_test = [
        "url",
        "firebase_id",
        "id",
        "room_id",
        "created_at",
        "updated_at",
    ]

    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=mock_room_photos,
        status=expected_status,
    )
    room_list_response = test_app.get(f"{API_URL}/rooms/{test_room_id}/photos")

    check_responses_equality(
        room_list_response.json(), mock_room_photos, list_attrs_to_test
    )
    for i, room_photo in enumerate(room_list_response.json()["room_photos"]):
        check_responses_equality(
            room_photo, mock_room_photos["room_photos"][i], attrs_to_test
        )


def test_delete_room_photo(test_app, monkeypatch):
    test_room_photo = MockRoomPhotoUploadResponse().dict()
    test_room_id = test_room_photo["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "url",
        "firebase_id",
        "id",
        "room_id",
        "created_at",
        "updated_at",
    ]

    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_photo,
            status=HTTP_201_CREATED,
        )
        upload_photo(test_app, test_room_id)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.DELETE,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_photo,
            status=expected_status,
        )
        room_response = test_app.delete(
            f"{API_URL}/rooms/{test_room_id}/photos/{test_room_photo['firebase_id']}"
        )

    assert room_response.status_code == expected_status
    check_responses_equality(room_response.json(), test_room_photo, attrs_to_test)


"""def test_add_and_get_room_photos(test_app, monkeypatch):
    mock_room_photos = MockRoomPhotoList().dict()
    test_room_photo = mock_room_photos["room_photos"][0]
    test_room_second_photo = mock_room_photos["room_photos"][1]
    test_room_id = mock_room_photos["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "url",
        "firebase_id",
        "id",
        "room_id",
        "created_at",
        "updated_at",
    ]

    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_photo,
            status=HTTP_201_CREATED,
        )
        upload_photo(test_app, test_room_id)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_second_photo,
            status=HTTP_201_CREATED,
        )
        upload_photo(test_app, test_room_id)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{POSTSERVER_API_URL}/{test_room_id}/photos/{test_room_photo['id']}",
            json=test_room_photo,
            status=expected_status,
        )
        room_response = test_app.get(
            f"{API_URL}/rooms/{test_room_id}/photos/{test_room_photo['firebase_id']}"
        )

        assert room_response.status_code == expected_status
        check_responses_equality(room_response.json(), test_room_photo, attrs_to_test)

        rsps.add(
            responses.GET,
            f"{POSTSERVER_API_URL}/{test_room_id}/photos/{test_room_second_photo['id']}",
            json=test_room_second_photo,
            status=expected_status,
        )
        room_response = test_app.get(
            f"{API_URL}/rooms/{test_room_id}/photos/{test_room_second_photo['firebase_id']}"
        )

        assert room_response.status_code == expected_status
        check_responses_equality(
            room_response.json(), test_room_second_photo, attrs_to_test
        )
"""
