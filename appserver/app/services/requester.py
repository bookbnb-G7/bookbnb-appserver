import logging
import os

import requests

logger = logging.getLogger(__name__)


class Requester:

    AUTH_SERVER_API_KEY = os.environ["AUTH_SERVER_API_KEY"]
    POST_SERVER_API_KEY = os.environ["POST_SERVER_API_KEY"]
    USER_SERVER_API_KEY = os.environ["USER_SERVER_API_KEY"]

    POST_API_URL = os.environ["POSTSERVER_URL"]
    AUTH_API_URL = os.environ["AUTHSERVER_URL"]
    USER_API_URL = os.environ["USERSERVER_URL"]

    @classmethod
    def room_srv_fetch(cls, method, path, payload=None, extra_headers=None):
        header = {"api-key": cls.POST_SERVER_API_KEY}

        if extra_headers is not None:
            header.update(extra_headers)

        if payload is None:
            payload = {}

        url = cls.POST_API_URL + path

        return cls._fetch(method, url, header, payload)

    @classmethod
    def auth_srv_fetch(cls, method, path, payload=None, extra_headers=None):
        header = {"api-key": cls.AUTH_SERVER_API_KEY}
        print(f"La api key del post server es: {header}")

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
        print(
            f"La url de user es: {url}, la env var resulto: \
                {os.environ['USERSERVER_URL']}"
        )

        return cls._fetch(method, url, header, payload)

    @classmethod
    def _fetch(cls, method, url, headers, payload):
        logger.info("Sending method %s to url: %s", method, url)
        logger.debug("Header: %s, payload %s", headers, payload)

        response = requests.request(method, url, json=payload, headers=headers)
        return response.json(), response.status_code
