import ssl
import http.client
from base64 import b64encode
from firewall import Firewall

class Constants(object):
  HTTP_SUCCESS = [200, 201, 202, 203, 204, 205, 206, 207]

class Opnsense(object):

  def __init__(self, api_key, api_secret, endpoint, ca_path=None):
    self._api_key = api_key
    self._api_secret = api_secret
    self._scheme = "https"
    self._endpoint = endpoint
    self._ca_path = ca_path
    self._context = None

    if ca_path is not None:
      self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
      self._context.load_verify_locations(ca_path)

    self._connection = http.client.HTTPSConnection(self._endpoint, self._context)

  @property
  def device_path(self):
    return f"{self._scheme}://{self._endpoint}"

  def authenticated_request(self, method, path, body=None, headers=None) -> http.client.HTTPResponse:
    if headers is None:
      headers = {}
    headers["Authorization"] = f"Basic {b64encode(self._api_key)}:{b64encode(self._api_secret)}"
    self._connection.request(method, f"{self.device_path}/api/{path}", body, headers)
    return self._connection.getresponse()

  @property
  def firewall(self) -> Firewall:
    return Firewall(self)