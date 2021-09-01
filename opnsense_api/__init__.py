import json
import ssl
import http.client
from base64 import b64encode
from opnsense_api.firewall import Firewall
from opnsense_api.util import Constants
import os.path

class Opnsense(object):

  def __init__(self, api_key, api_secret, host, port=443, scheme="https", ca_path=None):
    self._api_key = api_key
    self._api_secret = api_secret
    self._host = host
    self._port = port
    self._scheme = scheme
    self._ca_path = ca_path
    self._context = None

    # Base64 encode the api key and secret.
    # This will get passed as basic auth.
    self._b64_auth = b64encode(str.encode(f"{self._api_key}:{self._api_secret}")).decode("utf-8")

    if ca_path is not None:
      self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
      self._context.load_verify_locations(os.path.abspath(ca_path))

    self._connection = http.client.HTTPSConnection(
      host = self._host,
      port = self._port,
      context=self._context
    )

  @property
  def device_path(self):
    return f"{self._scheme}://{self._host}:{self._port}"

  def authenticated_request(self, method, path, body=None, headers=None) -> http.client.HTTPResponse:
    if headers is None:
      headers = {}
    headers["Authorization"] = f"Basic {self._b64_auth}"

    if (method == "POST") and (body is not None):
      headers["Content-Type"] = "application/json"

    if isinstance(body, (dict, list, tuple)):
      body = json.dumps(body)

    self._connection.request(method, f"{self.device_path}/api/{path}", body, headers)
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