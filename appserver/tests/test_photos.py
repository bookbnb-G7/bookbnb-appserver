import re

import responses
from app.services.authsender import AuthSender
from firebase_admin import storage
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.photo_upload_models import (MockFirebaseBucketResponse,
                                                   MockRoomPhotoList,
                                                   MockRoomPhotoUploadResponse)
from tests.mock_models.room_models import MockRoomResponse
from tests.mock_models.user_models import MockUserResponse
from tests.utils import (APPSERVER_URL, POSTSERVER_ROOM_REGEX, USER_REGEX,
                         check_responses_equality)


def upload_photo(test_app, test_room_id, header):
    test_files = {"file": ("test_image.png", b"laimageeennnrefake")}
    test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room_id}/photos", files=test_files, headers=header
    )


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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.PATCH,
        re.compile(USER_REGEX),
        json=mock_user_response.dict(),
        status=expected_status,
    )
    response = test_app.patch(
        f"{APPSERVER_URL}/users/{test_user_id}/photo", files=test_files, headers=header
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_upload_room_photo(test_app, monkeypatch):
    test_room_photo = MockRoomPhotoUploadResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user_id = 1
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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_photo,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room_id}/photos", files=test_files, headers=header
    )
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
    room_list_response = test_app.get(f"{APPSERVER_URL}/rooms/{test_room_id}/photos")

    check_responses_equality(
        room_list_response.json(), mock_room_photos, list_attrs_to_test
    )
    for i, room_photo in enumerate(room_list_response.json()["room_photos"]):
        check_responses_equality(
            room_photo, mock_room_photos["room_photos"][i], attrs_to_test
        )


@responses.activate
def test_delete_room_photo(test_app, monkeypatch):
    test_room_photo = MockRoomPhotoUploadResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user_id = 1
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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=expected_status,
    )
    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_photo,
        status=HTTP_201_CREATED,
    )
    upload_photo(test_app, test_room_id, header)

    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_photo,
        status=expected_status,
    )
    room_response = test_app.delete(
        f"{APPSERVER_URL}/rooms/{test_room_id}/photos/{test_room_photo['firebase_id']}",
        headers=header,
    )

    assert room_response.status_code == expected_status
    check_responses_equality(room_response.json(), test_room_photo, attrs_to_test)


"""
def test_add_and_get_room_photos(test_app, monkeypatch):
    test_room = MockRoomResponse().dict()
    mock_room_photos = MockRoomPhotoList().dict()
    test_user_id = 1
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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    monkeypatch.setattr(storage, "bucket", MockFirebaseBucketResponse)
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room,
            status=expected_status,
        )
        rsps.add(
            responses.POST,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_photo,
            status=HTTP_201_CREATED,
        )
        upload_photo(test_app, test_room_id, header)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room,
            status=expected_status,
        )
        rsps.add(
            responses.POST,
            re.compile(POSTSERVER_ROOM_REGEX),
            json=test_room_second_photo,
            status=HTTP_201_CREATED,
        )
        upload_photo(test_app, test_room_id, header)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{POST_API_URL}/rooms/{test_room_id}/photos/{test_room_photo['id']}",
            json=test_room_photo,
            status=expected_status,
        )
        room_response = test_app.get(
            f"{APPSERVER_URL}/rooms/{test_room_id}/photos/{test_room_photo['firebase_id']}"
        )

        assert room_response.status_code == expected_status
        check_responses_equality(room_response.json(), test_room_photo, attrs_to_test)

        rsps.add(
            responses.GET,
            f"{POST_API_URL}/rooms/{test_room_id}/photos/{test_room_second_photo['id']}",
            json=test_room_second_photo,
            status=expected_status,
        )
        room_response = test_app.get(
            f"{APPSERVER_URL}/rooms/{test_room_id}/photos/{test_room_second_photo['firebase_id']}"
        )

        assert room_response.status_code == expected_status
        check_responses_equality(
            room_response.json(), test_room_second_photo, attrs_to_test
        )
"""
