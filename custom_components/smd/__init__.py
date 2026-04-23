import logging

from .load_dashboard import load_dashboard
from .const import DOMAIN
from .process_yaml import async_process_yaml

from homeassistant.components import frontend

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    _LOGGER.info("Setting up SMD")
    
    hass.data[DOMAIN] = {
        "commands": {},
        'latest_version': ""
    }

    return True

async def async_setup_entry(hass, entry):
    _LOGGER.info("Setting up SMD entry")

    await async_process_yaml(hass, entry)

    load_dashboard(hass, entry)

    entry.add_update_listener(_update_listener) 

    return True


async def async_remove_entry(hass, config_entry):
    _LOGGER.info("Removing SMD")

    frontend.async_remove_panel(hass, "smd")


async def _update_listener(hass, config_entry):
    _LOGGER.info('Updating SMD listener')

    await async_process_yaml(hass, config_entry)

    hass.bus.async_fire("smd_reload")

    return True