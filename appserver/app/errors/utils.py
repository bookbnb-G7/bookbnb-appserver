from requests.models import Response


def get_error_message(response: Response):
    return response.json()["error"]
