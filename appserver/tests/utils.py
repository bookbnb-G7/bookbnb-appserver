import json
from typing import List, Dict, Any


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
