import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Configuration:
LANGUAGE = "language"
LANGUAGES = [
    "English",
    "Dutch"
]

@config_entries.HANDLERS.register(DOMAIN)
class SmDashboardConfigFlow(config_entries.ConfigFlow):
    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SmDashboardEditFlow(config_entry)

class SmDashboardEditFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = {
            vol.Optional(LANGUAGE, default=self.config_entry.options.get("language", "English")): vol.In(LANGUAGES)
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema)
        )
