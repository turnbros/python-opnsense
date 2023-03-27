import http.client
import http.client
import json
import logging
import os
import ssl
from base64 import b64encode

from opnsense_api.firewall import Firewall
from opnsense_api.interfaces import Interfaces
from opnsense_api.routing import Routing
from opnsense_api.unbound import Unbound
from opnsense_api.util import Constants, reliable_b64_decode

log = logging.getLogger(__name__)


class Opnsense(object):

    def __init__(self, api_key=None, api_secret=None, host=None, port=None, scheme=None, ca_path=None, ca_content=None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._host = host
        self._port = port
        self._scheme = scheme
        self._ca_path = ca_path
        self._ca_content = ca_content
        self._context = None

        # Check the environment variables to fill in any missing input variables
        if self._api_key is None:
            self._api_key = os.getenv("OPN_API_KEY", None)

        if self._api_secret is None:
            self._api_secret = os.getenv("OPN_API_SECRET", None)

        if self._scheme is None:
            self._scheme = os.getenv("OPN_API_SCHEME", "https")

        if self._host is None:
            self._host = os.getenv("OPN_API_HOST", None)

        if self._port is None:
            self._port = int(os.getenv("OPN_API_PORT", 443))

        if self._ca_path is None:
            self._ca_path = os.getenv("OPN_API_CA_PATH", None)

        if self._ca_content is None:
            self._ca_content = os.getenv("OPN_API_CA_CONTENT", None)

        # Raise an exception and quit if we're missing the key, secret, or host.
        if self._api_key is None:
            raise Exception("API key not found!")
        if self._api_secret is None:
            raise Exception("API secret not found!")
        if self._host is None:
            raise Exception("API host not found!")

        # Base64 encode the api key and secret.
        # This will get passed as basic auth.
        self._b64_auth = b64encode(str.encode(
            f"{self._api_key}:{self._api_secret}")).decode("utf-8")

        # We'll use CA files provided by path first, then content second.
        if self._ca_path is not None:
            self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self._context.load_verify_locations(self._ca_path)
        elif self._ca_content is not None:
            self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self._context.load_verify_locations(
                cadata=reliable_b64_decode(self._ca_content))

        self._connection = http.client.HTTPSConnection(
            host=self._host,
            port=self._port,
            context=self._context
        )

    @property
    def _device_path(self):
        return f"{self._scheme}://{self._host}:{self._port}"

    def _authenticated_request(self, method, path, body=None, headers=None) -> http.client.HTTPResponse:
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Basic {self._b64_auth}"

        if (method == "POST") and (body is not None):
            headers["Content-Type"] = "application/json_src"

        if isinstance(body, (dict, list, tuple)):
            body = json.dumps(body)

        self._connection.request(
            method, f"{self._device_path}/api/{path}", body, headers)
        query_response = self._connection.getresponse()

        if query_response.status not in Constants.HTTP_SUCCESS:
            del headers["Authorization"]
            exception_message = {
                "exception_message": f"API Request Failed!",
                "request_method": method,
                "request_path": path,
                "request_headers": headers,
                "request_body": body,
                "response_status": int(query_response.status),
                "response_message": str(query_response.read())
            }
            raise Exception(json.dumps(exception_message))

        return json.loads(query_response.read())

    @property
    def firewall(self) -> Firewall:
        return Firewall(self)

    @property
    def unbound_dns(self) -> Unbound:
        return Unbound(self)

    @property
    def interfaces(self) -> Interfaces:
        return Interfaces(self)

    @property
    def routing(self) -> Routing:
        return Routing(self)
