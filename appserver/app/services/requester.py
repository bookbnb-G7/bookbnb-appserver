import os
import logging
import requests
from json import JSONDecodeError
from app.errors.http_error import BadGatewayError


class Requester():

    AUTH_SERVER_TOKEN = ''#os.environ['AUTH_SERVER_TOKEN'] if os.environ['ENVIRONMENT'] != 'testing' else ''
    POST_SERVER_TOKEN = ''#os.environ['POST_SERVER_TOKEN'] if os.environ['ENVIRONMENT'] != 'testing' else ''
    USER_SERVER_TOKEN = ''#os.environ['ROOM_SERVER_TOKEN'] if os.environ['ENVIRONMENT'] != 'testing' else ''

    # tal vez estaria bueno meterlo en una env var
    POST_API_URL = "https://bookbnb-postserver.herokuapp.com"  
    AUTH_API_URL = "https://bookbnb-authserver.herokuapp.com" 
    USER_API_URL = "https://bookbnb-userserver.herokuapp.com" 

    #def room_srv_fetch(cls, method, url, extra_headers, payload):
    
    @classmethod
    def post_srv_fetch(cls, method, path, payload, extra_headers = None):
        header = {"x-client-token": cls.POST_SERVER_TOKEN}
        
        if extra_headers is not None:
            header.update(extra_headers)   
        
        url = POST_API_URL + path

        return cls._fetch(method, url, header, payload)
    

    @classmethod
    def auth_srv_fetch(cls, method, path, payload, extra_headers = None):
        header = {"x-client-token": cls.AUTH_SERVER_TOKEN}
        
        if extra_headers is not None:
            header.update(extra_headers)  

        url = AUTH_API_URL + path

        return cls._fetch(method, url, header, payload)


    @classmethod
    def user_srv_fetch(cls, method, path, payload, extra_headers = None):
        header = {"x-client-token": cls.USER_SERVER_TOKEN}
        
        if extra_headers is not None:
            header.update(extra_headers)  

        url = USER_API_URL + path

        return cls._fetch(method, url, header, payload)


    @classmethod
    def _fetch(cls, method, url, headers, payload):
        try:
            #cls.logger().info(f"Launching {method} request at {url}. Payload: {payload}")
            #cls.logger().debug(f"Using extra headers: {headers}")

            response = requests.request(method, url,
                                        json=payload,
                                        headers=headers)

            return response.json(), response.status_code


        #except (requests.exceptions.RequestException, JSONDecodeError) as e:
        except Exception as e:
            #cls.logger().error(
            #    f"Failed to contact {url} with method {method} and payload {payload}. Error: {e}")
            raise BadGatewayError()

