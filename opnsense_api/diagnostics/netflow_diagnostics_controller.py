from opnsense_api.util.controller import OPNsenseAPIController


class NetflowDiagnosticsController(OPNsenseAPIController):
    def __init__(self, device):
        super().__init__(device, "diagnostics", "netflow")

    def get_cache_stats(self):
        """
        Returns netflow cache stats

        :return:
        """
        return self._api_get("cacheStats")

    def get_config(self):
        """
        Returns the active netflow config

        :return:
        """
        return self._api_get("getconfig")

    def is_enabled(self):
        """
        Returns `True` if netflow data collection is enabled.

        :return: bool
        """

        return self._api_get("isEnabled")

    def reconfigure(self) -> None:  # This is POST
        """
        Applies any pending configuration changes.

        :return: None
        """
        return self._api_get("reconfigure")

    def set_config(self):  # This is GET?
        """
        Updates the netflow configuration

        :return:
        """
        return self._api_get("setconfig")

    def get_status(self):
        """
        Returns the status of netflow collection

        :return:
        """
        return self._api_get("status")


