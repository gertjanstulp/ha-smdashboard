import logging

from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.components.lovelace import _register_panel

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def load_dashboard(hass, entry):
    _LOGGER.info("Loading dashboard sm_dashboard")

    dashboard_url = "sm-dashboard"
    dashboard_config = {
        "mode": "yaml",
        "icon": "mdi:alpha-d-box",
        "title": "Dashboard",
        "filename": "lovelace/sm-dashboard/ui-lovelace.yaml",
        "show_in_sidebar": True,
        "require_admin": False,
    }

    hass.data["lovelace"]["dashboards"][dashboard_url] = LovelaceYAML(hass, dashboard_url, dashboard_config)

    _register_panel(hass, dashboard_url, "yaml", dashboard_config, False)