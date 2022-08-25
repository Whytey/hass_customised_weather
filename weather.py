"""
Provides the ability to create a customised weather component from existing 
Home-Assistant entities.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/weather.customised/
"""
import logging

import voluptuous as vol

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION, ATTR_FORECAST_PRECIPITATION, ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW, ATTR_FORECAST_TIME, ATTR_FORECAST_WIND_SPEED,
    ATTR_FORECAST_WIND_BEARING,
    PLATFORM_SCHEMA, WeatherEntity)
from homeassistant.const import (TEMP_CELSIUS, CONF_NAME, STATE_UNKNOWN)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = 'Data provided by your Home-Assistant entities'

DEFAULT_NAME = 'Customised Weather'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional("condition", default=None): cv.string,
    vol.Optional("temperature", default=None): cv.string,
    vol.Optional("humidty"): cv.string,
    vol.Optional("pressure"): cv.string,
    vol.Optional("windspeed"): cv.string,
    vol.Optional("wind_bearing"): cv.string,
    vol.Optional("temperature_unit"): cv.string,
    vol.Optional("ozone"): cv.string,
    vol.Optional("visibiliy"): cv.string,
    vol.Optional("forecast"): cv.string,

})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Customised weather platform."""

    name = config.get(CONF_NAME)
    condition = config.get("condition")
    temperature = config.get("temperature")

    add_entities([CustomisedWeather(
        name, condition, temperature, hass.config.units.temperature_unit, hass)], True)


class CustomisedWeather(WeatherEntity):
    """Implementation of CustomisedWeather WeatherEntity"""

    def __init__(self, name, condition, temperature, temperature_unit, hass):
        """Initialize the sensor."""
        self._name = name
        self._condition = condition
        self._temperature = temperature
        self._temperature_unit = temperature_unit
        self._hass = hass
        self.data = None
        self.forecast_data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def condition(self):
        """Return the current condition."""
        try:
            return self._hass.states.get(self._condition).state
        except AttributeError:
            return None

    @property
    def temperature(self):
        """Return the temperature."""
        try:
            return float(self._hass.states.get(self._temperature).state)
        except AttributeError:
            return None

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        return 80

    def update(self):
        """Get the latest data from entities and updates the states."""
        pass


