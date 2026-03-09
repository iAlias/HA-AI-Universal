"""HA AI Universal integration for Home Assistant."""

from .const import DOMAIN


async def async_setup(hass, config):
    """Set up the HA AI Universal integration.

    Args:
        hass: The Home Assistant instance.
        config: The Home Assistant configuration dictionary.

    Returns:
        True if setup was successful.
    """
    hass.data.setdefault(DOMAIN, {})
    return True
