import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.booking_models import (MockBookingAcceptedResponse,
                                              MockBookingListResponse,
                                              MockBookingRejectedResponse,
                                              MockBookingResponse,
                                              MockRoomBookingResponse)
from tests.mock_models.user_models import MockUserResponse
from tests.mock_models.room_models import MockRoomResponse
from tests.utils import (APPSERVER_URL, PAYMENT_BOOKING_ACCEPT_REGEX,
                         PAYMENT_BOOKING_REGEX, PAYMENT_BOOKING_REJECT_REGEX,
                         POSTSERVER_ROOM_BOOKING_REGEX, POSTSERVER_ROOM_REGEX,
                         USER_REGEX, check_responses_equality)


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
        "transaction_status": payment_payload["transactionStatus"],
        "created_at": payment_payload["createdAt"],
        "updated_at": payment_payload["updatedAt"],
    }

    return booking_camel


@responses.activate
def test_add_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_booking_payload = {
        "room_id": test_booking["roomId"],
        "date_from": test_booking["dateFrom"],
        "date_to": test_booking["dateTo"],
    }
    test_room_booking = MockRoomBookingResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    expected_status = HTTP_201_CREATED
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
    monkeypatch.setattr(AuthSender, "can_book_room", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_booking,
        status=expected_status,
    )
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/bookings",
        json=test_booking_payload,
        headers=header,
    )
    assert response.status_code == expected_status
    # TODO: Change BookingDB model to match camelcase in payment server
    test_camel = payment_camel_to_snake(test_booking)
    check_responses_equality(response.json(), test_camel, attrs_to_test)


# Mock accept
@responses.activate
def test_accept_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    test_booking_accepted = MockBookingAcceptedResponse().dict()
    booking_id = test_booking["id"]
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
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_BOOKING_ACCEPT_REGEX),
        json=test_booking_accepted,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/bookings/{booking_id}/accept", headers=header
    )
    assert response.status_code == expected_status
    # TODO: Change BookingDB model to match camelcase in payment server
    test_camel = payment_camel_to_snake(test_booking_accepted)
    check_responses_equality(response.json(), test_camel, attrs_to_test)


# Mock reject
@responses.activate
def test_reject_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_room = MockRoomResponse().dict()
    test_user = MockUserResponse().dict()
    test_booking_rejected = MockBookingRejectedResponse().dict()
    test_room_booking = MockRoomBookingResponse().dict()
    booking_id = test_booking["id"]
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
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_BOOKING_REJECT_REGEX),
        json=test_booking_rejected,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_booking,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/bookings/{booking_id}/reject", headers=header
    )
    assert response.status_code == expected_status
    # TODO: Change BookingDB model to match camelcase in payment server
    test_camel = payment_camel_to_snake(test_booking_rejected)
    check_responses_equality(response.json(), test_camel, attrs_to_test)


@responses.activate
def test_get_all_room_bookings(test_app):
    test_booking_list = MockBookingListResponse().dict()
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

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking_list,
        status=HTTP_200_OK,
    )

    response = test_app.get(f"{APPSERVER_URL}/bookings")
    response_json = response.json()
    assert response.status_code == expected_status

    # TODO: Change BookingDB model to match camelcase in payment server
    for i in range(len(test_booking_list)):
        test_booking_list[i] = payment_camel_to_snake(test_booking_list[i])

    booking_list = {"amount": len(test_booking_list), "bookings": test_booking_list}

    check_responses_equality(response_json, booking_list, ["amount"])

    for i, booking in enumerate(booking_list["bookings"]):
        check_responses_equality(booking, response_json["bookings"][i], attrs_to_test)


@responses.activate
def test_get_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_booking_id = test_booking["id"]
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

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )

    response = test_app.get(f"{APPSERVER_URL}/bookings/{test_booking_id}")
    assert response.status_code == expected_status

    # TODO: Change BookingDB model to match camelcase in payment server
    test_camel = payment_camel_to_snake(test_booking)
    check_responses_equality(response.json(), test_camel, attrs_to_test)


@responses.activate
def test_delete_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_booking_id = test_booking["id"]
    test_room_booking = MockRoomBookingResponse().dict()
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
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(PAYMENT_BOOKING_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room_booking,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/bookings/{test_booking_id}",
        headers=header,
    )
    assert response.status_code == expected_status

    # TODO: Change BookingDB model to match camelcase in payment server
    test_camel = payment_camel_to_snake(test_booking)
    check_responses_equality(response.json(), test_camel, attrs_to_test)
