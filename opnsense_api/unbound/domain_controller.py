import logging

from .controller import UnboundResource
from .util import format_request, DomainOverride

log = logging.getLogger(__name__)


class Domain(UnboundResource[DomainOverride]):

    def __init__(self, device):
        super().__init__(device, "domain")

    def add(self,
            domain: str,
            server: str,
            description: str = "",
            enabled: bool = True,
            ) -> DomainOverride:
        """
    Adds a domain override to Unbound

    :param domain: The domain to override DNS requests for.
    :param server: The IP address that the DNS requests will be sent to.
    :param description: The overrides' description.
    :param enabled: whether the override is enabled.
    :return: DomainOverride
    """

        request_body = {
            "domain": {
                "domain": domain,
                "server": server,
                "description": description,
                "enabled": str(int(enabled))
            }
        }

        request_base = format_request(self._module, self._controller, "addDomainOverride")
        response = self._device._authenticated_request("POST", request_base, body=request_body)
        if response['result'] != "saved":
            raise Exception(f"Failed to add domain override. Reason: {response}")

        self.apply_changes()
        return self.get(response['uuid'])

    def set(self,
            uuid: str,
            domain: str,
            server: str,
            description: str = "",
            enabled: bool = True,
            ) -> DomainOverride:
        """
    Update an attribute of a domain override

    :param uuid: The UUID of the override. This is generated when the override is created.
    :param domain: The domain to override DNS requests for.
    :param server: The IP address that the DNS requests will be sent to.
    :param description: The overrides' description.
    :param enabled: Whether the override is enabled.
    :return: DomainOverride
    """
        request_body = {
            "domain": {
                "domain": domain,
                "server": server,
                "description": description,
                "enabled": str(int(enabled))
            }
        }
        request_base = format_request(self._module, self._controller, "setDomainOverride", uuid)

        response = self._device._authenticated_request("POST", request_base, body=request_body)
        if response['result'] == "saved":
            self.apply_changes()
            return self.get(uuid)
        else:
            raise Exception(f"Failed to update domain override. Reason: {response}")
