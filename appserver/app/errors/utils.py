import json
from requests.models import Response


def get_error_message(response: Response):
    return json.dumps(response.json())
