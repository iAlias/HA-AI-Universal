"""HA AI Universal integration for Home Assistant."""

from .const import DOMAIN


async def async_setup(hass, config):
    """Set up the HA AI Universal integration."""
    hass.data.setdefault(DOMAIN, {})
    return True
