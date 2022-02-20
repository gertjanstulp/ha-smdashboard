import logging
from homeassistant.components.frontend import add_extra_js_url

DATA_EXTRA_MODULE_URL = 'frontend_extra_module_url'

_LOGGER = logging.getLogger(__name__)

def load_plugins(hass, name):
    _LOGGER.info("Loading plugins")

    # #Cards by others
    # add_extra_js_url(hass, "/sm_dashboard/cards/button-card/button-card.js")
    # add_extra_js_url(hass, "/sm_dashboard/cards/light-entity-card/light-entity-card.js")

    # Main by sm-dashboard
    add_extra_js_url(hass, "/sm_dashboard/js/sm-dashboard.js")

    # Cards by sm-dashboard
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-header-card/sm-header-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-heading-card/sm-heading-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-wrapper-card/sm-wrapper-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-flexbox-card/sm-flexbox-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-hash-switch-card/sm-hash-switch-card.js")
    # add_extra_js_url(hass, "/sm_dashboard/cards/sm-weather-card/sm-weather-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-notification-card/sm-notification-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-collapse-card/sm-collapse-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-cover-card/sm-cover-card.js")
    add_extra_js_url(hass, "/sm_dashboard/cards/sm-auto-entities-card/sm-auto-entities-card.js")

    hass.http.register_static_path("/sm_dashboard/js", hass.config.path(f"www/sm-dashboard/main"), True)
    hass.http.register_static_path("/sm_dashboard/cards", hass.config.path(f"www/sm-dashboard/cards"), True)