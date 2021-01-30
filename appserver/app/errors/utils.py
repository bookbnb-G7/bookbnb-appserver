import json
from requests.models import Response


def get_error_message(response: Response):
    err = "error"
    try:
        err = response.json()["error"]
    except AttributeError:
        err = "'error' attr not present, err: " + json.dumps(response.json())

    return err
