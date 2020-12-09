from json import JSONDecodeError
import os

import requests
from app.errors.http_error import BadGatewayError


class Requester:

    AUTH_SERVER_API_KEY = os.environ['AUTH_SERVER_API_KEY']
    POST_SERVER_API_KEY = os.environ['POST_SERVER_API_KEY']
    USER_SERVER_API_KEY = os.environ['USER_SERVER_API_KEY']

    # tal vez estaria bueno meterlo en una env var
    POST_API_URL = "https://bookbnb-postserver.herokuapp.com"
    AUTH_API_URL = "https://bookbnb-authserver.herokuapp.com"
    USER_API_URL = "https://bookbnb-userserver.herokuapp.com"

    # def room_srv_fetch(cls, method, url, extra_headers, payload):

    @classmethod
    def room_srv_fetch(cls, method, path, payload=None, extra_headers=None):
        header = {"api-key": cls.POST_SERVER_API_KEY}
        print(f"La api key del post server es: {cls.POST_SERVER_API_KEY}")

        if extra_headers is not None:
            header.update(extra_headers)

        if payload is None:
            payload = {}

        url = cls.POST_API_URL + path

        return cls._fetch(method, url, header, payload)

    @classmethod
    def auth_srv_fetch(cls, method, path, payload=None, extra_headers=None):
        header = {"api_key": cls.AUTH_SERVER_API_KEY}

        if extra_headers is not None:
            header.update(extra_headers)

        if payload is None:
            payload = {}

        url = cls.AUTH_API_URL + path

        return cls._fetch(method, url, header, payload)

    @classmethod
    def user_srv_fetch(cls, method, path, payload=None, extra_headers=None):
        header = {"api_key": cls.USER_SERVER_API_KEY}

        if extra_headers is not None:
            header.update(extra_headers)

        if payload is None:
            payload = {}

        url = cls.USER_API_URL + path

        return cls._fetch(method, url, header, payload)

    @classmethod
    def _fetch(cls, method, url, headers, payload):
        try:
            # cls.logger().info(f"Launching {method} request at {url}. Payload: {payload}")
            # cls.logger().debug(f"Using extra headers: {headers}")

            response = requests.request(method, url, json=payload, headers=headers)

            return response.json(), response.status_code

        # except (requests.exceptions.RequestException, JSONDecodeError) as e:
        except Exception as e:
            # cls.logger().error(
            #    f"Failed to contact {url} with method {method} and payload {payload}. Error: {e}")
            raise BadGatewayError() from e
