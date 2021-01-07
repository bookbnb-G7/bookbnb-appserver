import json
import os
from typing import Any, Dict, List

POST_API_URL = os.environ["POSTSERVER_URL"]
AUTH_API_URL = os.environ["AUTHSERVER_URL"]
USER_API_URL = os.environ["USERSERVER_URL"]
APPSERVER_URL = os.environ["APPSERVER_URL"]
PAYMENT_API_URL = os.environ["PAYMENT_URL"]

AUTH_REGEX = rf"{AUTH_API_URL}"
PAYMENT_BOOKING_REGEX = rf"{PAYMENT_API_URL}/bookings/?[0-9]*[/]?"
PAYMENT_BOOKING_ACCEPT_REGEX = rf"{PAYMENT_API_URL}/bookings/?[0-9]*[/]?accept/?"
PAYMENT_BOOKING_REJECT_REGEX = rf"{PAYMENT_API_URL}/bookings/?[0-9]*[/]?reject/?"
PAYMENT_ROOM_REGEX = rf"{PAYMENT_API_URL}/rooms/?[0-9]*[/]?"
PAYMENT_WALLET_REGEX = rf"{PAYMENT_API_URL}/wallets/?[0-9]*[/]?"
POSTSERVER_ROOM_REGEX = rf"{POST_API_URL}/rooms/?[0-9]*[/]?"
POSTSERVER_ROOM_BOOKING_REGEX = rf"{POST_API_URL}/rooms/?[0-9]*[/]?bookings/?"
APPSERVER_ROOM_REGEX = rf"{APPSERVER_URL}/rooms/?[0-9]*[/]?"
HOST_RATING_REGEX = rf"{USER_API_URL}/users/?[0-9]*[/]?host_ratings/?"
GUEST_RATING_REGEX = rf"{USER_API_URL}/users/?[0-9]*[/]?guest_ratings/?"
HOST_REVIEW_REGEX = rf"{USER_API_URL}/users/?[0-9]*[/]?host_reviews/?"
GUEST_REVIEW_REGEX = rf"{USER_API_URL}/users/?[0-9]*[/]?guest_reviews/?"
USER_REGEX = rf"{USER_API_URL}/?[0-9]*[/]?"
RATING_REGEX = rf"{POST_API_URL}/rooms/?[0-9]*[/]?ratings/?"
REVIEW_REGEX = rf"{POST_API_URL}/rooms/?[0-9]*[/]?reviews/?"
COMMENT_REGEX = rf"{POST_API_URL}/rooms/?[0-9]*[/]?comments/?"
APPSERVER_ME_REGEX = rf"{APPSERVER_URL}/me?"
APPSERVER_WALLET_REGEX = rf"{APPSERVER_URL}/me/wallet?"


class MockResponse:
    def dict(self):
        return {}

    def json(self):
        return json.dumps(self.dict())


def check_responses_equality(
    response: Dict[str, Any], test_response: Dict[str, Any], test_attrs: List[str]
):
    for attr in test_attrs:
        assert response[attr] == test_response[attr]
