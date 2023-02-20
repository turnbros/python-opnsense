from .route_controller import RouteController as Route


class Routing(object):

  def __init__(self, device):
    self._device = device

  @property
  def route_controller(self) -> Route:
    return Route(self._device)
