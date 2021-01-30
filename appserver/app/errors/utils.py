import json
from requests.models import Response


def get_error_message(response: Response):
    if response.json().error is not None:
        return response.json()["error"]
    return "'error' attr not present, err: " + json.dumps(response.json())
