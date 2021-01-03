import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK
from tests.mock_models.user_models import (MockUserResponse,
                                           MockPaymentWalletResponse)
from tests.utils import (USER_REGEX, APPSERVER_ME_REGEX,
                         APPSERVER_WALLET_REGEX, PAYMENT_WALLET_REGEX,
                         check_responses_equality)


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
    # GET {appserver_url}/users/me/wallet

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