import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK
from tests.mock_models.user_models import (MockUserResponse,
                                           MockPaymentWalletResponse)
from tests.mock_models.booking_models import MockBookingListResponse
from tests.mock_models.room_models import MockRoomListResponse
from tests.utils import (APPSERVER_URL, USER_REGEX, APPSERVER_ME_REGEX,
                         APPSERVER_WALLET_REGEX, PAYMENT_WALLET_REGEX,
                         PAYMENT_BOOKING_REGEX, check_responses_equality)


def payment_camel_to_snake(payment_payload):
    booking_camel = {
        "id": payment_payload["id"],
        "price": payment_payload["price"],
        "room_id": payment_payload["roomId"],
        "booker_id": payment_payload["bookerId"],
        "room_owner_id": payment_payload["roomOwnerId"],
        "date_from": payment_payload["dateFrom"],
        "date_to": payment_payload["dateTo"],
        "booking_status": payment_payload["bookingStatus"],
        "transaction_hash": payment_payload["transactionHash"],
        "transaction_status": payment_payload["transactionStatus"]
    }

    return booking_camel


@responses.activate
def test_get_self_user(test_app, monkeypatch):
    # GET {appserver_url}/me
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
    # GET {appserver_url}/me/wallet

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

# TODO: GET me/bookings, GET me/rooms


@responses.activate
def test_get_self_user_bookings(test_app, monkeypatch):
    # GET {appserver_url}/me/bookings

    test_bookings = MockBookingListResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "id",
        "price",
        "room_id",
        "booker_id",
        "room_owner_id",
        "date_from",
        "date_to",
        "booking_status",
        "transaction_hash",
        "transaction_status",
    ]
    header = {"x-access-token": "tokenrefalso"}
    test_user_id = 1

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_bookings,
        status=expected_status
    )
    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_bookings,
        status=expected_status
    )
    response = test_app.get(
        f"{APPSERVER_URL}/me/bookings",
        headers=header
    )

    assert response.status_code == expected_status
    response_json = response.json()

    # TODO: Change BookingDB model to match camelcase in payment server
    for i in range(len(test_bookings)):
        test_bookings[i] = payment_camel_to_snake(test_bookings[i])

    # Format response into {made, received}
    test_bookings_camel = {
        "made": {
            "amount": len(test_bookings),
            "bookings": test_bookings,
        },
        "received": {
            "amount": len(test_bookings),
            "bookings": test_bookings,
        }
    }

    check_responses_equality(response_json, test_bookings_camel, ["made", "received"])
    check_responses_equality(response_json["made"], test_bookings_camel["made"], ["amount", "bookings"])
    check_responses_equality(response_json["received"], test_bookings_camel["received"], ["amount", "bookings"])

    for i, booking in enumerate(test_bookings_camel["made"]["bookings"]):
        check_responses_equality(booking, response_json["made"]["bookings"][i], attrs_to_test)

    for i, booking in enumerate(test_bookings_camel["received"]["bookings"]):
        check_responses_equality(booking, response_json["received"]["bookings"][i], attrs_to_test)

'''
def test_get_self_user_rooms(test_app, monkeypatch):
    # GET {appserver_url}/me/rooms
'''
