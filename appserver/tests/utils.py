import json
import re
from typing import List, Dict, Any
import httpretty


class MockResponse:
    def dict(self):
        return {}

    def json(self):
        return json.dumps(self.dict())


def mock_request(method: str, mock_response, url_regex: str, expected_status: int):
    """
    Mocks http requests, returns a Response object with status "expected_status" and
    body equal to mock_response.json()

    Args:
        method (str): One of httpretty methods (httpretty.POST, httpretty.PATCH, etc)
        mock_response (MockObject): Object that must implement .json() method returning
        a dictionary
        url_regex (str): raw regex string (r"[0-9]*[/]?" for example) to match the
        desired URL
        expected_status (int): Status code of the returned Response object
    """
    httpretty.register_uri(
        method,
        re.compile(url_regex),
        responses=[
            httpretty.Response(body=mock_response.json(), status=expected_status)
        ],
    )


def check_responses_equality(
    response: Dict[str, Any], test_response: Dict[str, Any], test_attrs: List[str]
):
    for attr in test_attrs:
        assert response[attr] == test_response[attr]
