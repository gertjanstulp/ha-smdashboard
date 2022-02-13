import logging
import os
import logging
from collections import OrderedDict

from homeassistant.util.yaml import loader
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

def load_yamll(fname, secrets = None, args={}):
    try:
        _LOGGER.warn('sm dashboard')
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

_LOGGER.warning("test sm_dashboard")
loader.load_yaml = load_yamll
loader.SafeLineLoader.add_constructor("!include", _include_yaml)