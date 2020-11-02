import json
import pytest
from starlette.testclient import TestClient

from app.main import app


class MockResponse:
    def dict(self):
        pass

    def json(self):
        return json.dumps(self.dict())


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
