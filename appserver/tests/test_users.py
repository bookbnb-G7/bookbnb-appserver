import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.user_models import (MockUserListResponse,
                                           MockUserResponse,
                                           MockPaymentWalletResponse)
from tests.utils import (APPSERVER_URL, AUTH_REGEX, USER_REGEX,
                         APPSERVER_ME_REGEX, APPSERVER_WALLET_REGEX,
                         PAYMENT_WALLET_REGEX, check_responses_equality)


@responses.activate
def test_create_user(test_app, monkeypatch):
    test_user = MockUserResponse().dict()
    test_wallet = MockPaymentWalletResponse().dict()
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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    responses.add(
        responses.POST,
        re.compile(AUTH_REGEX),
        json={"email": test_user["email"], "uuid": test_user["id"]},
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(USER_REGEX),
        json=test_user,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_WALLET_REGEX),
        json=test_wallet,
        status=expected_status
    )
    response = test_app.post(f"{APPSERVER_URL}/users", json=test_user, headers=header)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_get_user_by_id(test_app):
    test_user = MockUserResponse().dict()
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
        json=test_user,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}")

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_get_self_user(test_app, monkeypatch):
    # GET {appserver_url}/users/me
    test_user = MockUserResponse().dict()
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
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=expected_status,
    )
    response = test_app.get(APPSERVER_ME_REGEX, headers=header)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_get_self_user_wallet(test_app, monkeypatch):
    # TODO: GET {appserver_url}/users/me/wallet

    test_wallet = MockPaymentWalletResponse().dict()
    test_user_id = 1
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "uuid",
        "address",
        "mnemonic",
    ]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.GET,
        re.compile(PAYMENT_WALLET_REGEX),
        json=test_wallet,
        status=expected_status,
    )
    response = test_app.get(APPSERVER_WALLET_REGEX, headers=header)

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_wallet, attrs_to_test)


@responses.activate
def test_edit_user(test_app, monkeypatch):
    test_full_user = MockUserResponse().dict()
    test_user_id = test_full_user["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = ["firstname", "lastname", "email", "phonenumber"]
    test_user = {attr: test_full_user[attr] for attr in attrs_to_test}
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.PATCH,
        re.compile(USER_REGEX),
        json=test_full_user,
        status=expected_status,
    )
    response = test_app.patch(
        f"{APPSERVER_URL}/users/{test_user_id}", json=test_user, headers=header
    )

    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user, attrs_to_test)


@responses.activate
def test_delete_user(test_app, monkeypatch):
    test_user = MockUserResponse().dict()
    test_user_id = test_user["id"]
    expected_status = HTTP_200_OK
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)
    responses.add(
        responses.DELETE,
        re.compile(USER_REGEX),
        json=test_user,
        status=expected_status,
    )
    response = test_app.delete(f"{APPSERVER_URL}/users/{test_user_id}", headers=header)

    assert response.status_code == expected_status


@responses.activate
def test_get_all_users(test_app):
    test_user_list = MockUserListResponse().dict()
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
        json=test_user_list,
        status=expected_status,
    )
    response = test_app.get(f"{APPSERVER_URL}/users")
    response_json = response.json()

    assert response.status_code == expected_status
    check_responses_equality(response_json, test_user_list, ["amount"])

    test_users = test_user_list["users"]
    response_users = response_json["users"]

    for i, user in enumerate(response_users):
        check_responses_equality(user, test_users[i], attrs_to_test)
