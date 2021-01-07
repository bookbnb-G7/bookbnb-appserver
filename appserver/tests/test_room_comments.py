import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.room_models import MockRoomResponse
from tests.mock_models.room_comments_models import (MockCommentResponse,
                                                    MockCommentListResponse)
from tests.mock_models.user_models import MockUserResponse
from tests.utils import (APPSERVER_URL, POSTSERVER_ROOM_REGEX, COMMENT_REGEX,
                         USER_REGEX, check_responses_equality)


@responses.activate
def test_post_room_comment(test_app, monkeypatch):
    test_comment = MockCommentResponse().dict()
    test_comment_payload = {
      "comment": test_comment["comment"],
      "main_comment_id": test_comment["main_comment_id"],
    }
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    expected_status = HTTP_201_CREATED
    attrs_to_test = ["comment", "commentator", "commentator_id", "main_comment_id", "id", "room_id"]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_comment", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_comment["commentator_id"]
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(COMMENT_REGEX),
        json=test_comment,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room['id']}/comments",
        json=test_comment_payload,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_comment, attrs_to_test)


@responses.activate
def test_get_all_room_comments(test_app):
    mock_comment_response = MockCommentListResponse()
    test_comment_list = mock_comment_response.dict()
    expected_status = HTTP_200_OK
    attrs_to_compare = ["amount", "room_id"]
    room_attrs_to_compare = ["comment", "commentator", "commentator_id", "main_comment_id", "id", "room_id"]

    responses.add(
        responses.GET,
        re.compile(COMMENT_REGEX),
        json=mock_comment_response.dict(),
        status=expected_status,
    )
    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_comment_list['room_id']}/comments"
    )
    assert response.status_code == expected_status

    response_json = response.json()
    response_comments = response_json["comments"]
    test_comments = test_comment_list["comments"]

    check_responses_equality(response.json(), test_comment_list, attrs_to_compare)
    for i, response_comment in enumerate(response_comments):
        check_responses_equality(
            response_comment["comment"], test_comments[i]["comment"], room_attrs_to_compare
        )
        for j, response_answer in enumerate(response_comment["answers"]):
          check_responses_equality(
            response_answer, test_comments[i]["answers"][j], room_attrs_to_compare
          )


@responses.activate
def test_delete_room_comment(test_app, monkeypatch):
    test_comment = MockCommentResponse().dict()
    test_comment_id = test_comment["id"]
    test_room_id = test_comment["room_id"]
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(
        AuthSender, "get_uuid_from_token", lambda x: test_comment["commentator_id"]
    )
    responses.add(
        responses.GET,
        re.compile(COMMENT_REGEX),
        json=test_comment,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(COMMENT_REGEX),
        json=test_comment,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/rooms/{test_room_id}/comments/{test_comment_id}", headers=header
    )
    assert response.status_code == expected_status
