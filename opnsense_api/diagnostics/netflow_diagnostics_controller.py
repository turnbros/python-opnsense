from opnsense_api.util.controller import OPNsenseAPIController


class NetflowDiagnosticsController(OPNsenseAPIController):
    def __init__(self, device):
        super().__init__(device, "diagnostics", "netflow")

    def get_cache_stats(self):
        return self._api_get("cacheStats")

    def get_config(self):
        return self._api_get("getconfig")

    def is_enabled(self):
        return self._api_get("isEnabled")

    def reconfigure(self):  # This is POST
        return self._api_get("reconfigure")

    def set_config(self):  # This is GET?
        return self._api_get("setconfig")

    def get_status(self):
        return self._api_get("status")


