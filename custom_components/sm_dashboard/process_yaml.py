import logging
import os
import io
import jinja2

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.translation import async_get_translations
from homeassistant.util.yaml import loader
from homeassistant.util.yaml.objects import NodeDictClass

from .const import DOMAIN, VERSION

from .jinja import fromjson, dayfromnow, windicon, now, weathericon

_LOGGER = logging.getLogger(__name__)

jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))

jinja.filters['fromjson'] = fromjson
jinja.filters['dayfromnow'] = dayfromnow
jinja.filters['windicon'] = windicon
jinja.globals['now'] = now
jinja.filters['weathericon'] = weathericon

sm_dashboard_global = {}
sm_dashboard_translations = {}
sm_dashboard_icons = {}
sm_dashboard_paths = {}
hass_resources = {}

LANGUAGES = {
    "English": "en",
    "Dutch": "nl"
}


async def async_load_yamll(hass: HomeAssistant, fname, secrets=None, args={}):
    return await hass.async_add_executor_job(load_yamll, fname, secrets, args)

 
def load_yamll(fname, secrets=None, args={}):
    _LOGGER.info("Load_yamll: %s", fname)
    try:
        _process_yaml = False
        with open(fname, encoding="utf-8") as f:
            if f.readline().lower().startswith(("# sm_dashboard")):
                _process_yaml = True
                _LOGGER.info("Marked as sm_dashboard: %s", fname)

        if _process_yaml:
            stream = io.StringIO(jinja.get_template(fname).render({
                **args,
                "_smd_global": sm_dashboard_global,
                "_smd_translations": sm_dashboard_translations,
                "_hass_resources": hass_resources,
                "_smd_icons": sm_dashboard_icons,
                "_smd_paths": sm_dashboard_paths,
            }))
            stream.name = fname
            return loader.yaml.load(stream, Loader=lambda _stream: loader.PythonSafeLoader(_stream, secrets)) or NodeDictClass()
        else:
            with open(fname, encoding="utf-8") as config_file:
                return loader.yaml.load(config_file, Loader=lambda stream: loader.PythonSafeLoader(stream, secrets)) or NodeDictClass()
    except loader.yaml.YAMLError as exc:
        _LOGGER.error(str(exc))
        raise HomeAssistantError(exc)
    except UnicodeDecodeError as exc:
        _LOGGER.error("Unable to read file %s: %s", fname, exc)
        raise HomeAssistantError(exc)


def _include_yaml(ldr, node):
    vars = {}
    additional = {}
    if isinstance(node.value, str):
        fn = node.value
    else:
        fn, vars, *additional = ldr.construct_sequence(node)
    fname = os.path.abspath(os.path.join(os.path.dirname(ldr.name), fn))
    try:
        yaml = load_yamll(fname, ldr.secrets, args=vars)
        if additional and isinstance(additional, list) and len(additional) > 0:
            yaml = NodeDictClass(yaml | additional[0])
        return loader._add_reference(yaml, ldr, node)
    except FileNotFoundError as exc:
        _LOGGER.error("Unable to include file %s: %s", fname, exc)
        raise HomeAssistantError(exc)


loader.load_yaml = load_yamll
loader.PythonSafeLoader.add_constructor("!include", _include_yaml)


async def async_process_yaml(hass, entry):

    _LOGGER.info('Start of function to process all yaml files!')

    if ("language" in entry.options):
        language = LANGUAGES[entry.options["language"]]
    else:
        language = "en"

    if os.path.exists(hass.config.path("lovelace/sm-dashboard/ui-lovelace.yaml")):
        await async_load_translations(hass, language)
        await async_load_icons(hass)
        await async_load_paths(hass)

        sm_dashboard_global.update(
            [
                ("version", VERSION),
                ("language", language),
                ("hass", hass)
            ]
        )

        hass.bus.async_fire("sm_dashboard_reload")

    async def handle_reload(call):
        # Service call to reload SM Theme config
        _LOGGER.info("Reload SM Dashboard Configuration")

        await async_reload_configuration(hass)

    # Register service sm_dashboard.reload
    hass.services.async_register(DOMAIN, "reload", handle_reload)

    async def _async_load_hass_translations(*args):
        await async_load_hass_translation(hass, language)

    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STARTED,
        _async_load_hass_translations,
    )

    _LOGGER.info('Finished function to process all yaml files!')


async def async_load_hass_translation(hass, language):
    try:
        hass_resources.update(await async_get_translations(hass, language, "entity_component"))
        hass_resources.update(await async_get_translations(hass, language, "entity"))
        hass_resources.update(await async_get_translations(hass, language, "state"))

    except:
        _LOGGER.exception("Error occured while loading hass translations")
        hass_resources.update({})


async def async_load_translations(hass, language: str):
    sm_dashboard_translations.clear()
    translations_file = hass.config.path(f"lovelace/sm-dashboard/resources/translations/{language}.yaml")
    if not os.path.exists(translations_file):
        return
    translations = await async_load_yamll(hass, translations_file)
    sm_dashboard_translations.update(translations[language])


async def async_load_icons(hass):
    sm_dashboard_icons.clear()
    icons_file = hass.config.path("lovelace/sm-dashboard/resources/icons.yaml")
    if not os.path.exists(icons_file):
        return
    icons = await async_load_yamll(hass, icons_file) 
    if isinstance(icons, dict):
        icons_data = icons.get("icons", {})
        if icons_data:
            sm_dashboard_icons.update(icons_data)


async def async_load_paths(hass):
    sm_dashboard_paths.clear()
    paths_file = hass.config.path("lovelace/sm-dashboard/resources/paths.yaml")
    if not os.path.exists(paths_file):
        return
    paths = await async_load_yamll(hass, paths_file)
    if isinstance(paths, dict):
        paths_data = paths.get("paths", {})
        if paths_data:
            sm_dashboard_paths.update(paths_data)


async def async_reload_configuration(hass):
    if os.path.exists(hass.config.path("lovelace/sm-dashboard/ui-lovelace.yaml")):
        await async_load_translations(hass, sm_dashboard_global["language"])
        await async_load_icons(hass)
        await async_load_paths(hass)

    hass.bus.async_fire("sm_dashboard_reload")
