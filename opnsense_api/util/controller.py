import urllib.parse
import logging

log = logging.getLogger(__name__)


class OPNsenseAPIController:
    def __init__(self, device, module, controller):
        self._device = device
        self._module = module
        self._controller = controller

    def _format_request(self, command: str, uuid: str = None, params=None) -> str:
        # Simplest url path for a request
        # e.g. api/unbound/settings/searchHostOverride
        base_request = f"{self._module}/{self._controller}/{command}"

        # Add in the UUID for a specific resource
        # e.g. api/unbound/settings/getHostOverride/2ce9672e-43a5-4462-9cf1-084964970862
        if uuid is not None:
            base_request = f"{self._module}/{self._controller}/{command}/{uuid}"

        # Sprinkle some url params on top.
        # e.g. api/unbound/settings/toggleHostOverride/2ce9672e-43a5-4462-9cf1-084964970862
        if len(params.keys()) > 0:
            base_request = f"{base_request}?{urllib.parse.urlencode(params)}"

        return base_request

    def _api_request(self, method: str, command: str, uuid: str = None, params: dict = None, body: dict = None) -> dict:

        if params is None:
            params = {}

        return self._device._authenticated_request(
        method,
        self._format_request(command, uuid, params),
        body=body
        )

    def _api_get(self, command: str, uuid: str = None, params: dict = None, body: dict = None):
        return self._api_request("GET", command, uuid, params, body)

    def _api_post(self, command: str, uuid: str = None, params: dict = None, body: dict = None):
        return self._api_request("POST", command, uuid, params, body)

    def _api_put(self, command: str, uuid: str = None, params: dict = None, body: dict = None):
        return self._api_request("PUT", command, uuid, params, body)

    def _api_delete(self, command: str, uuid: str = None, params: dict = None, body: dict = None):
        return self._api_request("DELETE", command, uuid, params, body)
