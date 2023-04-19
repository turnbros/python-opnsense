from opnsense_api.util.controller import OPNsenseAPIController


class NetflowDiagnosticsController(OPNsenseAPIController):
    def __init__(self, device):
        super().__init__(device, "diagnostics", "netflow")

    def get_cache_stats(self) -> dict:
        """
        Returns netflow cache stats

        """
        return self._api_get("cacheStats")

    def get_config(self) -> dict:
        """
        Returns the active netflow config

        """
        return self._api_get("getconfig")

    def is_enabled(self) -> bool:
        """
        Returns `True` if netflow data collection is enabled.

        """

        return self._api_get("isEnabled")

    def reconfigure(self) -> None:  # This is POST
        """
        Applies any pending configuration changes.

        """
        return self._api_get("reconfigure")

    def set_config(self):  # This is GET?
        """
        Updates the netflow configuration

        """
        return self._api_get("setconfig")

    def get_status(self):
        """
        Returns the status of netflow collection

        """
        return self._api_get("status")


