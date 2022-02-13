import logging

from .process_yaml import bootstrap
# from .notifications import notifications

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sm_dashboard"

async def async_setup(hass, config):
    hass.data[DOMAIN] = {
        "notifications": {},
        "commands": {},
        'latest_version': ""
    }

    # notifications(hass, DOMAIN)
    
    bootstrap()

    return True

async def async_setup_entry(hass, entry):
    return True


async def async_remove_entry(hass, entry):
    return True
