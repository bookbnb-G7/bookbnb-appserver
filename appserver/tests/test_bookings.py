import re

import responses
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from tests.mock_models.booking_models import (MockBookingListResponse,
                                              MockBookingResponse,
                                              MockUserBookingListResponse,
                                              MockUserBookingResponse,
                                              MockPaymentBookingResponse,
                                              MockBookingAcceptedResponse,
                                              MockPaymentBookingAcceptedResponse,
                                              MockPaymentBookingRejectedResponse)
from tests.mock_models.room_models import MockRoomResponse
from tests.utils import (APPSERVER_URL, POSTSERVER_ROOM_REGEX, USER_REGEX,
                         POSTSERVER_ROOM_BOOKING_REGEX,
                         PAYMENT_BOOKING_REGEX, PAYMENT_BOOKING_ACCEPT_REGEX,
                         PAYMENT_BOOKING_REJECT_REGEX, check_responses_equality)


@responses.activate
def test_add_room_booking(test_app, monkeypatch):
    # return value of post to payment server
    test_booking_payment = MockPaymentBookingResponse().dict()

    # return value of post to post server
    test_booking = MockBookingResponse().dict()
    test_booking_payload = {
        "date_begins": test_booking["date_begins"],
        "date_ends": test_booking["date_ends"],
        "amount_of_people": test_booking["amount_of_people"],
        "user_id": test_booking["user_id"]
    }
    test_room = MockRoomResponse().dict()
    test_user_booking = MockUserBookingResponse().dict()
    test_user_id = test_booking["user_id"]
    test_room_id = test_room["owner_uuid"]
    expected_status = HTTP_201_CREATED
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]
    header = {"x-access-token": "tokenrefalso"}

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
        json=test_booking_payment,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.POST,
        re.compile(USER_REGEX),
        json=test_user_booking,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room_id}/bookings",
        json=test_booking_payload,
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_booking, attrs_to_test)


# Mock accept
@responses.activate
def test_accept_room_booking(test_app, monkeypatch):
    test_room = MockRoomResponse().dict()
    test_booking_accepted = MockBookingAcceptedResponse().dict()
    test_booking_id = test_booking_accepted["id"]
    test_user_id = test_booking_accepted["user_id"]
    test_room_id = test_booking_accepted["room_id"]
    test_payment_booking_accepted = MockPaymentBookingAcceptedResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]

    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_room,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_BOOKING_ACCEPT_REGEX),
        json=test_payment_booking_accepted,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.PATCH,
        re.compile(POSTSERVER_ROOM_BOOKING_REGEX),
        json=test_booking_accepted,
        status=HTTP_200_OK,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room_id}/bookings/{test_booking_id}/accept",
        headers=header
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_booking_accepted, attrs_to_test)


# Mock reject
@responses.activate
def test_reject_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_booking_id = test_booking["id"]
    test_user_id = test_booking["user_id"]
    test_room_id = test_booking["room_id"]
    test_payment_booking_rejected = MockPaymentBookingRejectedResponse().dict()
    test_user_booking = MockUserBookingResponse().dict()
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]

    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.POST,
        re.compile(PAYMENT_BOOKING_REJECT_REGEX),
        json=test_payment_booking_rejected,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_BOOKING_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )
    responses.add(
        responses.DELETE,
        re.compile(USER_REGEX),
        json=test_user_booking,
        status=expected_status,
    )
    response = test_app.post(
        f"{APPSERVER_URL}/rooms/{test_room_id}/bookings/{test_booking_id}/reject",
        headers=header
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_booking, attrs_to_test)


@responses.activate
def test_get_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_room_id = test_booking["room_id"]
    test_booking_id = test_booking["id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking,
        status=HTTP_200_OK,
    )

    response = test_app.get(
        f"{APPSERVER_URL}/rooms/{test_room_id}/bookings/{test_booking_id}"
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_booking, attrs_to_test)


@responses.activate
def test_get_all_room_bookings(test_app):
    test_booking_list = MockBookingListResponse().dict()
    test_room_id = test_booking_list["room_id"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking_list,
        status=HTTP_200_OK,
    )

    response = test_app.get(f"{APPSERVER_URL}/rooms/{test_room_id}/bookings/")
    response_json = response.json()
    assert response.status_code == expected_status
    check_responses_equality(response_json, test_booking_list, ["amount", "room_id"])

    for i, booking in enumerate(test_booking_list["bookings"]):
        check_responses_equality(booking, response_json["bookings"][i], attrs_to_test)


@responses.activate
def test_delete_room_booking(test_app, monkeypatch):
    test_booking = MockBookingResponse().dict()
    test_booking_id = test_booking["id"]
    test_room = MockRoomResponse().dict()
    test_user_booking = MockUserBookingResponse().dict()
    test_user_id = test_booking["user_id"]
    test_room_id = test_room["owner_uuid"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "user_id",
        "amount_of_people",
        "id",
        "room_id",
        "total_price",
        "status",
    ]
    header = {"x-access-token": "tokenrefalso"}

    monkeypatch.setattr(AuthSender, "is_valid_token", lambda x: True)
    monkeypatch.setattr(AuthSender, "has_permission_to_modify", lambda x, y: True)
    monkeypatch.setattr(AuthSender, "get_uuid_from_token", lambda x: test_user_id)

    responses.add(
        responses.GET,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(POSTSERVER_ROOM_REGEX),
        json=test_booking,
        status=expected_status,
    )
    responses.add(
        responses.DELETE,
        re.compile(USER_REGEX),
        json=test_user_booking,
        status=expected_status,
    )
    response = test_app.delete(
        f"{APPSERVER_URL}/rooms/{test_room_id}/bookings/{test_booking_id}",
        headers=header,
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_booking, attrs_to_test)


@responses.activate
def test_get_user_booking(test_app):
    test_user_booking = MockUserBookingResponse().dict()
    test_booking_id = test_user_booking["booking_id"]
    test_user_id = 3
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "booking_id",
        "room_id",
    ]

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_user_booking,
        status=HTTP_200_OK,
    )

    response = test_app.get(
        f"{APPSERVER_URL}/users/{test_user_id}/bookings/{test_booking_id}"
    )
    assert response.status_code == expected_status
    check_responses_equality(response.json(), test_user_booking, attrs_to_test)


@responses.activate
def test_get_all_user_bookings(test_app):
    test_booking_list = MockUserBookingListResponse().dict()
    test_user_id = test_booking_list["userId"]
    expected_status = HTTP_200_OK
    attrs_to_test = [
        "booking_id",
        "room_id",
    ]

    responses.add(
        responses.GET,
        re.compile(USER_REGEX),
        json=test_booking_list,
        status=HTTP_200_OK,
    )

    response = test_app.get(f"{APPSERVER_URL}/users/{test_user_id}/bookings/")
    response_json = response.json()
    assert response.status_code == expected_status
    check_responses_equality(response_json, test_booking_list, ["amount", "userId"])

    for i, booking in enumerate(test_booking_list["roomBookings"]):
        check_responses_equality(
            booking, response_json["roomBookings"][i], attrs_to_test
        )
