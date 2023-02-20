from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from dataclasses import dataclass, field
import logging

log = logging.getLogger(__name__)


@dataclass
class LoopbackInterface(OPNsenseItem):
  device_id: int = field(metadata={"json_name": "deviceId"})
  description: str


class LoopbackController(OPNsenseItemController[LoopbackInterface]):

  def __init__(self, device):
    super().__init__(device, "interface", "loopback_settings")

  def _parse_api_response(self, api_response: dict) -> LoopbackInterface:
    return LoopbackInterface(
      uuid=api_response["uuid"],
      device_id=api_response["deviceId"],
      description=api_response["description"]
    )

  def add(self, interface: LoopbackInterface) -> LoopbackInterface:
    pass

  def set(self, interface: LoopbackInterface) -> LoopbackInterface:
    pass
