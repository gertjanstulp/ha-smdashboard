import logging

from .const import DOMAIN
from .process_yaml import process_yaml
# from .notifications import notifications

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    hass.data[DOMAIN] = {
        "notifications": {},
        "commands": {},
        'latest_version': ""
    }

    # notifications(hass, DOMAIN)
    
    return True

async def async_setup_entry(hass, config_entry):
    process_yaml(hass, config_entry)

    config_entry.add_update_listener(_update_listener) 

    return True

async def _update_listener(hass, config_entry):
    _LOGGER.warning('Update_listener called')

    process_yaml(hass, config_entry)

    hass.bus.async_fire("sm_dashboard_reload")

    return True