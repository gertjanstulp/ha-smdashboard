import logging
import os
import logging
import json
import io
import jinja2
from collections import OrderedDict

from homeassistant.util.yaml import loader
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)

def fromjson(value):
    return json.loads(value)

jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))

jinja.filters['fromjson'] = fromjson

sm_dashboard_global = {}

def load_yamll(fname, secrets = None, args={}):
    _LOGGER.info("Load_yamll: %s", fname)
    try:
        
        process_yaml = False
        with open(fname, encoding="utf-8") as f:
            if f.readline().lower().startswith(("# sm_dashboard")):
                process_yaml = True
                _LOGGER.info("Marked as sm_dashboard: %s", fname)

        if process_yaml:
            stream = io.StringIO(jinja.get_template(fname).render({
                **args,
                "_dd_global": sm_dashboard_global
                }))
            stream.name = fname
            return loader.yaml.load(stream, Loader=lambda _stream: loader.SafeLineLoader(_stream, secrets)) or OrderedDict()
        else:
            with open(fname, encoding="utf-8") as config_file:
                return loader.yaml.load(config_file, Loader=lambda stream: loader.SafeLineLoader(stream, secrets)) or OrderedDict()
    except loader.yaml.YAMLError as exc:
        _LOGGER.error(str(exc))
        raise HomeAssistantError(exc)
    except UnicodeDecodeError as exc:
        _LOGGER.error("Unable to read file %s: %s", fname, exc)
        raise HomeAssistantError(exc)

def _include_yaml(ldr, node):
    args = {}
    if isinstance(node.value, str):
        fn = node.value
    else:
        fn, args, *_ = ldr.construct_sequence(node)
    fname = os.path.abspath(os.path.join(os.path.dirname(ldr.name), fn))
    try:
        return loader._add_reference(load_yamll(fname, ldr.secrets, args=args), ldr, node)
    except FileNotFoundError as exc:
        _LOGGER.error("Unable to include file %s: %s", fname, exc);
        raise HomeAssistantError(exc)

loader.load_yaml = load_yamll
loader.SafeLineLoader.add_constructor("!include", _include_yaml)

def process_yaml(hass, entry):

    _LOGGER.info('Start of function to process all yaml files!')

    if os.path.exists(hass.config.path("lovelace/sm-dashboard/ui-lovelace.yaml")):
        if os.path.exists(hass.config.path("custom_components/sm_dashboard/.installed")):
            installed = "true"
        else:
            installed = "false"

        sm_dashboard_global.update(
            [
                ("version", VERSION),
                ("installed", installed)
            ]
        )

        hass.bus.async_fire("sm_dashboard_reload")

    async def handle_reload(call):
        #Service call to reload SM Theme config
        _LOGGER.info("Reload SM Dashboard Configuration")

        reload_configuration(hass)

    # Register service sm_dashboard.reload
    hass.services.async_register(DOMAIN, "reload", handle_reload)


    async def handle_installed(call):
        #Service call to Change the installed key in global config for SM dashboard
        _LOGGER.info("Handle installed")

        path = hass.config.path("custom_components/sm_dashboard/.installed")

        if not os.path.exists(path):
            _LOGGER.info("Create .installed file")
            open(path, 'w').close()

        reload_configuration(hass)

    # Register service sm_dashboard.installed
    hass.services.async_register(DOMAIN, "installed", handle_installed)

    _LOGGER.info('Finished function to process all yaml files!')


def reload_configuration(hass):
    if os.path.exists(hass.config.path("lovelace/sm-dashboard/ui-lovelace.yaml")):
        if os.path.exists(hass.config.path("custom_components/sm_dashboard/.installed")):
            installed = "true"
        else:
            installed = "false"

        sm_dashboard_global.update(
            [
                ("installed", installed)
            ]
        )
        
    hass.bus.async_fire("sm_dashboard_reload")